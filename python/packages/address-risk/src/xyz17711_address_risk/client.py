"""Typed HTTP client for address-risk-service -- one method per operation, each with a sync form and an async (`a`-prefixed) form."""

from __future__ import annotations

import logging

from xyz17711_core import Client as _BaseClient

from .models import *  # noqa: F401,F403 -- re-exported for callers building requests

logger = logging.getLogger(__name__)


class Client(_BaseClient):
    """Typed client for address-risk-service. Every method has a sync form and an async form (the `a`-prefixed sibling, e.g. `acheck_address` next to `check_address`) sharing the same underlying connection/wallet -- pick whichever fits your own code."""

    def check_address(self, request: CheckAddressRequest) -> CheckAddressResponse:
        """Wallet address risk check: sanctioned address and phishing check for a crypto wallet or contract before you send funds, with theft, scam, mixer and blacklist flags ($0.005, x402)"""
        logger.debug("check_address: calling %s", "/v1/address-risk/check_address")
        return CheckAddressResponse.model_validate(self._post("/v1/address-risk/check_address", request.model_dump(mode="json", exclude_none=True)))

    async def acheck_address(self, request: CheckAddressRequest) -> CheckAddressResponse:
        """Wallet address risk check: sanctioned address and phishing check for a crypto wallet or contract before you send funds, with theft, scam, mixer and blacklist flags ($0.005, x402) (async)"""
        logger.debug("acheck_address: calling %s", "/v1/address-risk/check_address")
        return CheckAddressResponse.model_validate(await self._apost("/v1/address-risk/check_address", request.model_dump(mode="json", exclude_none=True)))

