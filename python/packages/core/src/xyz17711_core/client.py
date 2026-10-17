"""Core HTTP client for the 17711.xyz microservice fleet -- shared transport, auth, x402 payment,
and error handling every per-service generated client package builds on. Not meant to be used
directly beyond that -- see the top-level README for the full workflow these packages are
produced by.

Every generated method has both a sync and an async form (``tool_name`` / ``atool_name``) built on
the SAME underlying :class:`Client` instance -- a caller picks whichever fits their own code
(a plain script vs. an asyncio/LangChain agent) without constructing two separate client objects.
The async HTTP client is constructed lazily, on first async use, so a purely-sync caller never
pays for it.

x402 payment logic here implements the real x402 v2 protocol end to end: the same wire format
(three headers, base64-encoded JSON), the same EIP-3009 `transferWithAuthorization` signing over
EIP-712 typed data, and the same per-call/cumulative spend-cap discipline a careful buyer
implementation needs. Payment decision/signing is pure, I/O-free logic shared identically by the
sync and async request paths -- never duplicated between them.
"""

from __future__ import annotations

import base64
import json
import logging
import secrets
import threading
import time
from typing import Any, Awaitable, Callable, Optional

import httpx

logger = logging.getLogger(__name__)

HEADER_PAYMENT_REQUIRED = "PAYMENT-REQUIRED"
HEADER_PAYMENT_SIGNATURE = "PAYMENT-SIGNATURE"
HEADER_PAYMENT_RESPONSE = "PAYMENT-RESPONSE"
USDC_DECIMALS = 6

# Cumulative x402 spend is tracked per WALLET ADDRESS, module-level, guarded by one lock shared by
# every `Client` instance in this process -- never a per-instance counter. Mirrors the Rust
# reference implementation's own deliberate choice (`nimpoleon-payment/src/client.rs`'s global
# `Mutex<f64>`): the idiomatic way to use this SDK is one `Client` per service (each generated
# `XToolkit` builds its own), so a per-instance counter would let the SAME wallet silently spend
# its configured cap once per client instead of once, total -- and even on a single instance, the
# check-then-increment sequence needs a lock to stay correct if a future change (or a caller
# driving this client from multiple threads, e.g. LangChain's sync tools running in a
# `ThreadPoolExecutor`) ever puts an `await`/context switch between the check and the increment.
_spend_lock = threading.Lock()
_cumulative_spent_by_address: dict[str, float] = {}


class PlatformError(Exception):
    """Mirrors this platform's own standardized error envelope
    (``{"error": {code, index, status, message}}``) -- every non-2xx response from any
    17711.xyz service raises this (or the more specific :class:`PaymentRequiredError` subclass
    below for a 402), never a bare ``httpx.HTTPStatusError``.
    """

    def __init__(self, code: str, index: int, status: int, message: str):
        self.code = code
        self.index = index
        self.status = status
        self.message = message
        super().__init__(f"{code}: {message}")

    @classmethod
    def from_response(cls, response: httpx.Response) -> "PlatformError":
        logger.debug("PlatformError.from_response: status=%s", response.status_code)
        try:
            error = response.json()["error"]
            err = cls(
                code=error.get("code", "unknown"),
                index=error.get("index", -1),
                status=error.get("status", response.status_code),
                message=error.get("message", response.text),
            )
        except Exception:
            err = cls(
                code="unknown",
                index=-1,
                status=response.status_code,
                message=response.text or f"HTTP {response.status_code}",
            )
        logger.error(
            "platform error: code=%s status=%s message=%s", err.code, err.status, err.message
        )
        return err


class PaymentRequiredError(PlatformError):
    """Raised when a gated tool's free quota is exhausted and either no wallet is configured on
    this :class:`Client`, or the seller's own accepted network doesn't match
    ``x402_expected_network``. Carries the decoded ``PAYMENT-REQUIRED`` challenge so a caller (a
    human, or a LangChain ``HumanInTheLoopMiddleware`` predicate) can decide what to do -- this is
    NOT a generic failure, it's an actionable "pay this much, on this network, to this address"
    signal.
    """

    def __init__(self, message: str, price_usdc: float, network: str, pay_to: str):
        self.price_usdc = price_usdc
        self.network = network
        self.pay_to = pay_to
        super().__init__(code="request.payment_required", index=-1, status=402, message=message)


class WalletConfigError(ValueError):
    """Raised by :class:`Client`'s constructor when ``x402_private_key`` is set but the rest of
    the wallet config is missing/incoherent -- a half-configured wallet with real funds behind it
    is worse to silently half-work than to refuse to start."""


def _decode_header(value: str) -> Optional[dict]:
    """Trims before base64-decoding an x402 wire header, ``None`` on any malformed input, never a
    raised exception."""
    logger.debug("_decode_header: decoding a %d-char header value", len(value))
    try:
        return json.loads(base64.b64decode(value.strip()))
    except Exception as e:
        logger.error("_decode_header: failed to decode header: %s", e)
        return None


def _encode_header(value: dict) -> str:
    logger.debug("_encode_header: encoding payload with keys=%s", list(value.keys()))
    return base64.b64encode(json.dumps(value).encode("utf-8")).decode("ascii")


def _parse_eip155_chain_id(network: str) -> int:
    logger.debug("_parse_eip155_chain_id: network=%s", network)
    if not network.startswith("eip155:"):
        logger.error("_parse_eip155_chain_id: malformed network id: %s", network)
        raise PlatformError(
            code="payment.invalid",
            index=-1,
            status=500,
            message=f'malformed network id (expected CAIP-2 "eip155:<chain_id>"): {network}',
        )
    return int(network[len("eip155:") :])


class Client:
    """Base HTTP client for one 17711.xyz service instance. Per-service generated client classes
    (e.g. ``xyz17711_proxy_pool.Client``) subclass this and add one sync + one async method per
    tool.

    x402 payment: OFF by default (a gated tool beyond its free quota raises
    :class:`PaymentRequiredError`). Pass ``x402_private_key`` (plus the three other
    ``x402_*`` parameters, all required together) to pay automatically -- requires the
    ``payments`` extra (``pip install xyz17711[payments]``) for ``eth-account``. The private key is
    read from wherever the CALLER sources it (an env var, a secrets manager); this class never
    reads an env var itself and never logs/prints the key.
    """

    def __init__(
        self,
        base_url: str,
        *,
        timeout: float = 30.0,
        x402_private_key: Optional[str] = None,
        x402_expected_network: Optional[str] = None,
        x402_max_payment_usdc: Optional[float] = None,
        x402_max_total_spend_usdc: Optional[float] = None,
    ):
        logger.debug(
            "Client.__init__: base_url=%s wallet_configured=%s",
            base_url,
            bool(x402_private_key),
        )
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._http = httpx.Client(base_url=self._base_url, timeout=timeout)
        self._ahttp: Optional[httpx.AsyncClient] = None  # lazy -- see module docstring

        self._account = None
        self._x402_expected_network = x402_expected_network
        self._x402_max_payment_usdc = x402_max_payment_usdc
        self._x402_max_total_spend_usdc = x402_max_total_spend_usdc

        if x402_private_key:
            missing = [
                name
                for name, value in (
                    ("x402_expected_network", x402_expected_network),
                    ("x402_max_payment_usdc", x402_max_payment_usdc),
                    ("x402_max_total_spend_usdc", x402_max_total_spend_usdc),
                )
                if value is None
            ]
            if missing:
                logger.error("Client.__init__: incoherent wallet config, missing=%s", missing)
                raise WalletConfigError(
                    "x402_private_key was set but "
                    + ", ".join(missing)
                    + " -- a wallet with real funds needs explicit per-call and cumulative spend"
                    " caps and an expected network, all set together, or none at all."
                )
            try:
                from eth_account import Account
            except ImportError as e:
                logger.error("Client.__init__: eth-account is not installed")
                raise WalletConfigError(
                    "x402_private_key was set but the `eth-account` package isn't installed --"
                    ' run `pip install "xyz17711[payments]"`.'
                ) from e
            self._account = Account.from_key(x402_private_key)
            logger.debug(
                "Client.__init__: wallet configured, address=%s expected_network=%s",
                self._account.address,
                x402_expected_network,
            )

    def _async_http(self) -> httpx.AsyncClient:
        if self._ahttp is None:
            logger.debug("Client._async_http: lazily constructing AsyncClient for %s", self._base_url)
            self._ahttp = httpx.AsyncClient(base_url=self._base_url, timeout=self._timeout)
        return self._ahttp

    def close(self) -> None:
        logger.debug("Client.close: closing sync HTTP client for %s", self._base_url)
        self._http.close()

    async def aclose(self) -> None:
        logger.debug("Client.aclose: closing async HTTP client for %s", self._base_url)
        self._http.close()
        if self._ahttp is not None:
            await self._ahttp.aclose()

    def __enter__(self) -> "Client":
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    async def __aenter__(self) -> "Client":
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        await self.aclose()

    # -- sync request helpers, used by every generated sync method --------------------------

    def _post(self, path: str, json_body: dict) -> Any:
        logger.debug("Client._post: path=%s", path)
        return self._request_with_payment(
            lambda headers: self._http.post(path, json=json_body, headers=headers)
        )

    def _get(self, path: str, params: dict) -> Any:
        logger.debug("Client._get: path=%s", path)
        clean_params = {k: v for k, v in params.items() if v is not None}
        return self._request_with_payment(
            lambda headers: self._http.get(path, params=clean_params, headers=headers)
        )

    def _request_with_payment(self, send: Callable[[dict], httpx.Response]) -> Any:
        first = send({})
        if first.status_code != 402:
            if not first.is_success:
                raise PlatformError.from_response(first)
            return first.json()

        signed_header = self._handle_402(first)
        second = send({HEADER_PAYMENT_SIGNATURE: signed_header})
        if not second.is_success:
            raise PlatformError.from_response(second)
        return second.json()

    # -- async request helpers, used by every generated async (`a...`) method ---------------

    async def _apost(self, path: str, json_body: dict) -> Any:
        logger.debug("Client._apost: path=%s", path)
        return await self._arequest_with_payment(
            lambda headers: self._async_http().post(path, json=json_body, headers=headers)
        )

    async def _aget(self, path: str, params: dict) -> Any:
        logger.debug("Client._aget: path=%s", path)
        clean_params = {k: v for k, v in params.items() if v is not None}
        return await self._arequest_with_payment(
            lambda headers: self._async_http().get(path, params=clean_params, headers=headers)
        )

    async def _arequest_with_payment(
        self, send: Callable[[dict], Awaitable[httpx.Response]]
    ) -> Any:
        first = await send({})
        if first.status_code != 402:
            if not first.is_success:
                raise PlatformError.from_response(first)
            return first.json()

        signed_header = self._handle_402(first)
        second = await send({HEADER_PAYMENT_SIGNATURE: signed_header})
        if not second.is_success:
            raise PlatformError.from_response(second)
        return second.json()

    # -- shared payment decision logic (pure/CPU-only -- no I/O, safe to share as-is between
    #    the sync and async request paths above, never duplicated) -------------------------

    def _handle_402(self, response: httpx.Response) -> str:
        """Given a 402 response, decodes the challenge and either returns a signed
        ``PAYMENT-SIGNATURE`` header value ready to retry with, or raises
        (:class:`PaymentRequiredError` if no wallet is configured / no matching network, or
        :class:`PlatformError` if a spend cap would be exceeded)."""
        logger.debug("Client._handle_402: received a 402, decoding challenge")
        header_value = response.headers.get(HEADER_PAYMENT_REQUIRED)
        if not header_value:
            logger.error("Client._handle_402: 402 with no PAYMENT-REQUIRED header")
            raise PlatformError(
                code="payment.invalid",
                index=-1,
                status=402,
                message="seller returned 402 with no PAYMENT-REQUIRED header",
            )
        payment_required = _decode_header(header_value)
        if payment_required is None:
            logger.error("Client._handle_402: PAYMENT-REQUIRED header did not decode to JSON")
            raise PlatformError(
                code="payment.invalid",
                index=-1,
                status=402,
                message="seller's PAYMENT-REQUIRED header did not decode to valid JSON",
            )

        requirements = next(
            (
                a
                for a in payment_required.get("accepts", [])
                if a.get("scheme") == "exact" and a.get("network") == self._x402_expected_network
            ),
            None,
        )
        amount_usdc = None
        if requirements is not None:
            amount_usdc = int(requirements["amount"]) / (10**USDC_DECIMALS)

        if self._account is None or requirements is None:
            logger.debug(
                "Client._handle_402: no wallet configured or no matching network -- raising PaymentRequiredError"
            )
            raise PaymentRequiredError(
                message=payment_required.get("error")
                or "this tool's free quota is used up -- sign and send a payment to continue",
                price_usdc=amount_usdc or 0.0,
                network=self._x402_expected_network or "",
                pay_to=(requirements or {}).get("payTo", ""),
            )

        if amount_usdc > self._x402_max_payment_usdc:
            logger.error(
                "Client._handle_402: amount %s USDC exceeds per-call cap %s",
                amount_usdc,
                self._x402_max_payment_usdc,
            )
            raise PlatformError(
                code="payment.rejected",
                index=-1,
                status=402,
                message=(
                    f"requested amount ({amount_usdc} USDC) exceeds this wallet's configured "
                    "per-call cap (x402_max_payment_usdc)"
                ),
            )
        address = self._account.address
        with _spend_lock:
            spent_so_far = _cumulative_spent_by_address.get(address, 0.0)
            if spent_so_far + amount_usdc > self._x402_max_total_spend_usdc:
                logger.error(
                    "Client._handle_402: would exceed cumulative cap for wallet %s (spent so far=%s, cap=%s)",
                    address,
                    spent_so_far,
                    self._x402_max_total_spend_usdc,
                )
                raise PlatformError(
                    code="payment.rejected",
                    index=-1,
                    status=402,
                    message=(
                        "paying this would exceed this wallet's configured cumulative cap "
                        "(x402_max_total_spend_usdc)"
                    ),
                )
            # Reserve the spend BEFORE signing (not after) so two concurrent calls on this same
            # wallet can never both pass the check above against the same `spent_so_far` -- a
            # signing failure below rolls this reservation back.
            _cumulative_spent_by_address[address] = spent_so_far + amount_usdc

        try:
            signed_header = self._sign_payment(payment_required, requirements)
        except Exception:
            with _spend_lock:
                _cumulative_spent_by_address[address] = (
                    _cumulative_spent_by_address.get(address, 0.0) - amount_usdc
                )
            raise

        logger.debug(
            "Client._handle_402: signed a payment for %s USDC (cumulative now %s for wallet %s)",
            amount_usdc,
            _cumulative_spent_by_address[address],
            address,
        )
        return signed_header

    def _sign_payment(self, payment_required: dict, requirements: dict) -> str:
        logger.debug(
            "Client._sign_payment: network=%s asset=%s", requirements["network"], requirements["asset"]
        )
        from eth_account.messages import encode_typed_data

        chain_id = _parse_eip155_chain_id(requirements["network"])
        now = int(time.time())
        valid_after = max(0, now - 60)
        valid_before = now + int(requirements["maxTimeoutSeconds"])
        nonce_bytes = secrets.token_bytes(32)
        nonce_hex = "0x" + nonce_bytes.hex()

        typed_data = {
            "types": {
                "EIP712Domain": [
                    {"name": "name", "type": "string"},
                    {"name": "version", "type": "string"},
                    {"name": "chainId", "type": "uint256"},
                    {"name": "verifyingContract", "type": "address"},
                ],
                "TransferWithAuthorization": [
                    {"name": "from", "type": "address"},
                    {"name": "to", "type": "address"},
                    {"name": "value", "type": "uint256"},
                    {"name": "validAfter", "type": "uint256"},
                    {"name": "validBefore", "type": "uint256"},
                    {"name": "nonce", "type": "bytes32"},
                ],
            },
            "primaryType": "TransferWithAuthorization",
            "domain": {
                "name": requirements["extra"]["name"],
                "version": requirements["extra"]["version"],
                "chainId": chain_id,
                "verifyingContract": requirements["asset"],
            },
            "message": {
                "from": self._account.address,
                "to": requirements["payTo"],
                "value": int(requirements["amount"]),
                "validAfter": valid_after,
                "validBefore": valid_before,
                "nonce": nonce_hex,
            },
        }

        signable = encode_typed_data(full_message=typed_data)
        signed = self._account.sign_message(signable)
        signature_hex = "0x" + signed.signature.hex().removeprefix("0x")

        authorization = {
            "from": self._account.address,
            "to": requirements["payTo"],
            "value": str(int(requirements["amount"])),
            "validAfter": str(valid_after),
            "validBefore": str(valid_before),
            "nonce": nonce_hex,
        }
        payload = {
            "x402Version": payment_required["x402Version"],
            "resource": payment_required.get("resource"),
            "accepted": requirements,
            "payload": {"signature": signature_hex, "authorization": authorization},
        }
        # x402 v2: echo the challenge's `extensions` (notably `bazaar`) back unchanged so the
        # facilitator can catalog the resource once this payment settles. Omitted when absent.
        if payment_required.get("extensions"):
            payload["extensions"] = payment_required["extensions"]
        logger.debug("Client._sign_payment: signature produced, nonce=%s", nonce_hex)
        return _encode_header(payload)
