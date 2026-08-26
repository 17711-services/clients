"""Typed HTTP client for ip-blocklist -- one method per operation, each with a sync form and an async (`a`-prefixed) form."""

from __future__ import annotations

import logging

from xyz17711_core import Client as _BaseClient

from .models import *  # noqa: F401,F403 -- re-exported for callers building requests

logger = logging.getLogger(__name__)


class Client(_BaseClient):
    """Typed client for ip-blocklist. Every method has a sync form and an async form (the `a`-prefixed sibling, e.g. `acheck_ip` next to `check_ip`) sharing the same underlying connection/wallet -- pick whichever fits your own code."""

    def check_ip(self, ip: str) -> CheckIpResponse:
        """Checks whether an IPv4 address appears on any of several public IP blocklists ($0.002, x402)"""
        logger.debug("check_ip: calling %s", "/v1/ip-blocklist/check")
        return CheckIpResponse.model_validate(self._get("/v1/ip-blocklist/check", {"ip": ip}))

    async def acheck_ip(self, ip: str) -> CheckIpResponse:
        """Checks whether an IPv4 address appears on any of several public IP blocklists ($0.002, x402) (async)"""
        logger.debug("acheck_ip: calling %s", "/v1/ip-blocklist/check")
        return CheckIpResponse.model_validate(await self._aget("/v1/ip-blocklist/check", {"ip": ip}))

