"""Typed HTTP client for ping-service -- one method per operation, each with a sync form and an async (`a`-prefixed) form."""

from __future__ import annotations

import logging

from xyz17711_core import Client as _BaseClient

from .models import *  # noqa: F401,F403 -- re-exported for callers building requests

logger = logging.getLogger(__name__)


class Client(_BaseClient):
    """Typed client for ping-service. Every method has a sync form and an async form (the `a`-prefixed sibling, e.g. `aping` next to `ping`) sharing the same underlying connection/wallet -- pick whichever fits your own code."""

    def ping(self, request: PingRequest) -> PingResult:
        """x402 ping: the cheapest end-to-end payment test for an x402 client or agent wallet, returns an echo and the server pid ($0.002, x402)"""
        logger.debug("ping: calling %s", "/v1/ping")
        return PingResult.model_validate(self._post("/v1/ping", request.model_dump(mode="json", exclude_none=True)))

    async def aping(self, request: PingRequest) -> PingResult:
        """x402 ping: the cheapest end-to-end payment test for an x402 client or agent wallet, returns an echo and the server pid ($0.002, x402) (async)"""
        logger.debug("aping: calling %s", "/v1/ping")
        return PingResult.model_validate(await self._apost("/v1/ping", request.model_dump(mode="json", exclude_none=True)))

