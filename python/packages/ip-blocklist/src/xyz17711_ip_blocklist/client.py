"""Typed HTTP client for ip-blocklist -- one method per operation, each with a sync form and an async (`a`-prefixed) form."""

from __future__ import annotations

import logging
from typing import Optional

from xyz17711_core import Client as _BaseClient

from .models import *  # noqa: F401,F403 -- re-exported for callers building requests

logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = "https://api.17711.xyz/registry/ip-blocklist"
"""Production base URL of this service; pass another `base_url` to self-host or test."""


class Client(_BaseClient):
    """Typed client for ip-blocklist. Every method has a sync form and an async form (the `a`-prefixed sibling, e.g. `acheck_ip` next to `check_ip`) sharing the same underlying connection/wallet -- pick whichever fits your own code."""

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        *,
        timeout: float = 30.0,
        x402_private_key: Optional[str] = None,
        x402_expected_network: Optional[str] = None,
        x402_max_payment_usdc: Optional[float] = None,
        x402_max_total_spend_usdc: Optional[float] = None,
    ):
        super().__init__(
            base_url,
            timeout=timeout,
            x402_private_key=x402_private_key,
            x402_expected_network=x402_expected_network,
            x402_max_payment_usdc=x402_max_payment_usdc,
            x402_max_total_spend_usdc=x402_max_total_spend_usdc,
        )

    def check_ip(self, ip: str) -> CheckIpResponse:
        """IP reputation check: is this IPv4 address on a public threat blocklist (Tor exit nodes, botnets, spam networks) ($0.010, x402)"""
        logger.debug("check_ip: calling %s", "/v1/ip-blocklist/check")
        return CheckIpResponse.model_validate(self._get("/v1/ip-blocklist/check", {"ip": ip}))

    async def acheck_ip(self, ip: str) -> CheckIpResponse:
        """IP reputation check: is this IPv4 address on a public threat blocklist (Tor exit nodes, botnets, spam networks) ($0.010, x402) (async)"""
        logger.debug("acheck_ip: calling %s", "/v1/ip-blocklist/check")
        return CheckIpResponse.model_validate(await self._aget("/v1/ip-blocklist/check", {"ip": ip}))

