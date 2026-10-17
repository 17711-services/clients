"""Typed HTTP client for proxy-pool -- one method per operation, each with a sync form and an async (`a`-prefixed) form."""

from __future__ import annotations

import logging
from typing import Optional

from xyz17711_core import Client as _BaseClient

from .models import *  # noqa: F401,F403 -- re-exported for callers building requests

logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = "https://api.17711.xyz/registry/proxy-pool"
"""Production base URL of this service; pass another `base_url` to self-host or test."""


class Client(_BaseClient):
    """Typed client for proxy-pool. Every method has a sync form and an async form (the `a`-prefixed sibling, e.g. `aget_best_proxy` next to `get_best_proxy`) sharing the same underlying connection/wallet -- pick whichever fits your own code."""

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

    def get_best_proxy(self, anonymity: Optional[str] = None, city: Optional[str] = None, country: Optional[str] = None, protocol: Optional[str] = None) -> GetBestProxyResponse:
        """Free proxy API: get one fast, verified-alive proxy (HTTP, SOCKS) filtered by country, protocol and anonymity, for scraping ($0.010, x402)"""
        logger.debug("get_best_proxy: calling %s", "/v1/proxy-pool/get_best_proxy")
        return GetBestProxyResponse.model_validate(self._get("/v1/proxy-pool/get_best_proxy", {"anonymity": anonymity, "city": city, "country": country, "protocol": protocol}))

    async def aget_best_proxy(self, anonymity: Optional[str] = None, city: Optional[str] = None, country: Optional[str] = None, protocol: Optional[str] = None) -> GetBestProxyResponse:
        """Free proxy API: get one fast, verified-alive proxy (HTTP, SOCKS) filtered by country, protocol and anonymity, for scraping ($0.010, x402) (async)"""
        logger.debug("aget_best_proxy: calling %s", "/v1/proxy-pool/get_best_proxy")
        return GetBestProxyResponse.model_validate(await self._aget("/v1/proxy-pool/get_best_proxy", {"anonymity": anonymity, "city": city, "country": country, "protocol": protocol}))

