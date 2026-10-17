"""Typed HTTP client for token-verdict-service -- one method per operation, each with a sync form and an async (`a`-prefixed) form."""

from __future__ import annotations

import logging

from xyz17711_core import Client as _BaseClient

from .models import *  # noqa: F401,F403 -- re-exported for callers building requests

logger = logging.getLogger(__name__)


class Client(_BaseClient):
    """Typed client for token-verdict-service. Every method has a sync form and an async form (the `a`-prefixed sibling, e.g. `aget_verdict` next to `get_verdict`) sharing the same underlying connection/wallet -- pick whichever fits your own code."""

    def get_verdict(self, request: GetVerdictRequest) -> GetVerdictResponse:
        """Token verdict and security check: is this token safe? Honeypot, rug pull and scam detection with taxes, liquidity and admin powers ($0.01, x402)"""
        logger.debug("get_verdict: calling %s", "/v1/token-verdict/get_verdict")
        return GetVerdictResponse.model_validate(self._post("/v1/token-verdict/get_verdict", request.model_dump(mode="json", exclude_none=True)))

    async def aget_verdict(self, request: GetVerdictRequest) -> GetVerdictResponse:
        """Token verdict and security check: is this token safe? Honeypot, rug pull and scam detection with taxes, liquidity and admin powers ($0.01, x402) (async)"""
        logger.debug("aget_verdict: calling %s", "/v1/token-verdict/get_verdict")
        return GetVerdictResponse.model_validate(await self._apost("/v1/token-verdict/get_verdict", request.model_dump(mode="json", exclude_none=True)))

