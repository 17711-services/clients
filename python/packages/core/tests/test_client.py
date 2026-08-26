"""Real functional tests for xyz17711_core.Client -- the x402 payment port in particular, since
that logic (EIP-712 signing, retry-after-402, spend caps) is genuinely new code, not a thin
wrapper. Uses httpx.MockTransport throughout -- no real network call, no real blockchain
interaction -- but exercises the REAL signing path via a real (freshly generated, unfunded) test
account from eth_account, so a malformed signature would be caught here."""

from __future__ import annotations

import asyncio

import httpx
import pytest
from eth_account import Account

import xyz17711_core.client as client_module
from xyz17711_core.client import (
    PaymentRequiredError,
    PlatformError,
    WalletConfigError,
    _decode_header,
    _encode_header,
)
from xyz17711_core import Client

TEST_PRIVATE_KEY = Account.create().key.hex()
TEST_ADDRESS = Account.from_key(TEST_PRIVATE_KEY).address


@pytest.fixture(autouse=True)
def _reset_shared_spend_tracker():
    """The cumulative x402 spend tracker is module-level, keyed by wallet address, shared by every
    `Client` instance in this process (see `client.py`'s own doc comment on `_spend_lock`) -- tests
    reusing `TEST_ADDRESS` would otherwise leak spend state into each other depending on run order.
    """
    client_module._cumulative_spent_by_address.clear()
    yield
    client_module._cumulative_spent_by_address.clear()

PAYMENT_REQUIRED_BODY = {
    "x402Version": 2,
    "error": "PAYMENT-SIGNATURE header is required",
    "resource": {
        "url": "https://example.test/tool",
        "description": "",
        "mimeType": "application/json",
    },
    "accepts": [
        {
            "scheme": "exact",
            "network": "eip155:84532",
            "amount": "10000",
            "asset": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
            "payTo": "0x209693Bc6afc0C5328bA36FaF03C514EF312287C",
            "maxTimeoutSeconds": 60,
            "extra": {"name": "USDC", "version": "2"},
        }
    ],
}


def _mock_client(handler, **client_kwargs) -> Client:
    """A Client wired to a fake transport for BOTH its sync and async HTTP clients -- see
    `generate.py`'s own identical helper for why both need mocking."""
    client = Client("https://example.test", **client_kwargs)
    client._http = httpx.Client(base_url="https://example.test", transport=httpx.MockTransport(handler))
    client._ahttp = httpx.AsyncClient(
        base_url="https://example.test", transport=httpx.MockTransport(handler)
    )
    return client


def _paid_wallet_kwargs(**overrides):
    kwargs = dict(
        x402_private_key=TEST_PRIVATE_KEY,
        x402_expected_network="eip155:84532",
        x402_max_payment_usdc=1.0,
        x402_max_total_spend_usdc=100.0,
    )
    kwargs.update(overrides)
    return kwargs


def _payment_required_response() -> httpx.Response:
    return httpx.Response(402, headers={"PAYMENT-REQUIRED": _encode_header(PAYMENT_REQUIRED_BODY)})


class TestHeaderCodec:
    def test_round_trips_a_real_payload(self):
        encoded = _encode_header(PAYMENT_REQUIRED_BODY)
        decoded = _decode_header(encoded)
        assert decoded == PAYMENT_REQUIRED_BODY

    def test_trims_surrounding_whitespace(self):
        encoded = _encode_header(PAYMENT_REQUIRED_BODY)
        assert _decode_header(f"  {encoded}\n") == PAYMENT_REQUIRED_BODY

    def test_returns_none_for_garbage(self):
        assert _decode_header("not valid base64 or json!!!") is None


class TestNoWallet:
    def test_sync_post_without_wallet_raises_payment_required(self):
        client = _mock_client(lambda r: _payment_required_response())
        with pytest.raises(PaymentRequiredError):
            client._post("/v1/tool", {})

    def test_async_apost_without_wallet_raises_payment_required(self):
        client = _mock_client(lambda r: _payment_required_response())
        with pytest.raises(PaymentRequiredError):
            asyncio.run(client._apost("/v1/tool", {}))

    def test_sync_get_without_wallet_raises_payment_required(self):
        client = _mock_client(lambda r: _payment_required_response())
        with pytest.raises(PaymentRequiredError):
            client._get("/v1/tool", {"q": "x"})


class TestSuccessfulPayment:
    def _handler_factory(self):
        calls = {"n": 0}

        def handler(request: httpx.Request) -> httpx.Response:
            calls["n"] += 1
            if request.headers.get("PAYMENT-SIGNATURE"):
                payload = _decode_header(request.headers["PAYMENT-SIGNATURE"])
                assert payload["x402Version"] == 2
                assert payload["accepted"]["network"] == "eip155:84532"
                auth = payload["payload"]["authorization"]
                assert auth["from"].lower() == TEST_ADDRESS.lower()
                assert auth["to"] == "0x209693Bc6afc0C5328bA36FaF03C514EF312287C"
                assert auth["value"] == "10000"
                assert payload["payload"]["signature"].startswith("0x")
                assert len(payload["payload"]["signature"]) == 2 + 130  # 0x + 65 bytes hex
                return httpx.Response(200, json={"ok": True})
            return _payment_required_response()

        return handler, calls

    def test_sync_post_pays_and_retries(self):
        handler, calls = self._handler_factory()
        client = _mock_client(handler, **_paid_wallet_kwargs())
        result = client._post("/v1/tool", {})
        assert result == {"ok": True}
        assert calls["n"] == 2
        assert abs(client_module._cumulative_spent_by_address[TEST_ADDRESS] - 0.01) < 1e-9

    def test_async_apost_pays_and_retries(self):
        handler, calls = self._handler_factory()
        client = _mock_client(handler, **_paid_wallet_kwargs())
        result = asyncio.run(client._apost("/v1/tool", {}))
        assert result == {"ok": True}
        assert calls["n"] == 2

    def test_sync_get_pays_and_retries(self):
        handler, calls = self._handler_factory()
        client = _mock_client(handler, **_paid_wallet_kwargs())
        result = client._get("/v1/tool", {"q": "hello", "unset": None})
        assert result == {"ok": True}
        assert calls["n"] == 2


class TestCapsAndValidation:
    def test_per_call_cap_rejects_before_signing(self):
        calls = {"n": 0}

        def handler(request):
            calls["n"] += 1
            return _payment_required_response()

        client = _mock_client(handler, **_paid_wallet_kwargs(x402_max_payment_usdc=0.001))
        with pytest.raises(PlatformError) as exc_info:
            client._post("/v1/tool", {})
        assert exc_info.value.code == "payment.rejected"
        assert calls["n"] == 1  # never retried -- rejected before a second request was ever sent

    def test_cumulative_cap_rejects_second_call(self):
        handler, _ = TestSuccessfulPayment()._handler_factory()
        client = _mock_client(
            handler, **_paid_wallet_kwargs(x402_max_total_spend_usdc=0.015)
        )
        client._post("/v1/tool", {})  # first call: 0.01 USDC, within the 0.015 cap
        with pytest.raises(PlatformError) as exc_info:
            client._post("/v1/tool", {})  # second call would bring total to 0.02 > 0.015
        assert exc_info.value.code == "payment.rejected"

    @staticmethod
    def _paid_handler(request: httpx.Request) -> httpx.Response:
        # Unlike `TestSuccessfulPayment._handler_factory`, deliberately does NOT assert a specific
        # signer address -- these two tests exercise MULTIPLE distinct wallets against the same
        # handler, so it just confirms a signature was attached before granting a 200.
        if request.headers.get("PAYMENT-SIGNATURE"):
            return httpx.Response(200, json={"ok": True})
        return _payment_required_response()

    def test_cumulative_cap_is_shared_across_client_instances_for_the_same_wallet(self):
        # The regression test for the module-level-per-address tracker (see `client.py`'s own
        # `_spend_lock` doc comment): the idiomatic use of this SDK is one `Client` per service, so
        # the SAME wallet used to construct two separate `Client`s must still be capped as ONE
        # wallet, not reset to a fresh budget on every new instance.
        client_a = _mock_client(self._paid_handler, **_paid_wallet_kwargs(x402_max_total_spend_usdc=0.015))
        client_b = _mock_client(self._paid_handler, **_paid_wallet_kwargs(x402_max_total_spend_usdc=0.015))
        client_a._post("/v1/tool", {})  # 0.01 USDC via client_a, within the shared 0.015 cap
        with pytest.raises(PlatformError) as exc_info:
            client_b._post("/v1/tool", {})  # same wallet, a DIFFERENT instance -- still capped
        assert exc_info.value.code == "payment.rejected"

    def test_different_wallets_have_independent_cumulative_caps(self):
        key_a, key_b = Account.create().key.hex(), Account.create().key.hex()
        client_a = _mock_client(
            self._paid_handler,
            **_paid_wallet_kwargs(x402_private_key=key_a, x402_max_total_spend_usdc=0.015),
        )
        client_b = _mock_client(
            self._paid_handler,
            **_paid_wallet_kwargs(x402_private_key=key_b, x402_max_total_spend_usdc=0.015),
        )
        client_a._post("/v1/tool", {})
        client_b._post("/v1/tool", {})  # a different wallet -- must not be blocked by client_a's spend

    def test_network_mismatch_raises_payment_required_not_a_silent_wrong_chain_payment(self):
        client = _mock_client(
            lambda r: _payment_required_response(),
            **_paid_wallet_kwargs(x402_expected_network="eip155:1"),
        )
        with pytest.raises(PaymentRequiredError):
            client._post("/v1/tool", {})

    @pytest.mark.parametrize(
        "missing_kwarg",
        ["x402_expected_network", "x402_max_payment_usdc", "x402_max_total_spend_usdc"],
    )
    def test_incoherent_wallet_config_raises_at_construction(self, missing_kwarg):
        kwargs = _paid_wallet_kwargs()
        kwargs[missing_kwarg] = None
        with pytest.raises(WalletConfigError):
            Client("https://example.test", **kwargs)

    def test_no_wallet_at_all_is_a_valid_configuration(self):
        # Constructing a Client with none of the x402_* kwargs must never raise -- payment is
        # strictly opt-in.
        Client("https://example.test")


class TestRegressionAgainstNonPaymentBehavior:
    def test_plain_2xx_success_is_unaffected(self):
        client = _mock_client(lambda r: httpx.Response(200, json={"echoed": "hi"}))
        assert client._post("/v1/echo", {"x": 1}) == {"echoed": "hi"}

    def test_plain_non_402_error_still_raises_platform_error_not_payment_required(self):
        client = _mock_client(
            lambda r: httpx.Response(
                500,
                json={
                    "error": {
                        "code": "internal.unhandled",
                        "index": 9999,
                        "status": 500,
                        "message": "boom",
                    }
                },
            )
        )
        with pytest.raises(PlatformError) as exc_info:
            client._post("/v1/echo", {})
        assert not isinstance(exc_info.value, PaymentRequiredError)
        assert exc_info.value.code == "internal.unhandled"
