"""Typed HTTP client for 🚫 sanctions-check-service -- one method per operation, each with a sync form and an async (`a`-prefixed) form."""

from __future__ import annotations

import logging

from xyz17711_core import Client as _BaseClient

from .models import *  # noqa: F401,F403 -- re-exported for callers building requests

logger = logging.getLogger(__name__)


class Client(_BaseClient):
    """Typed client for 🚫 sanctions-check-service. Every method has a sync form and an async form (the `a`-prefixed sibling, e.g. `ascreen_name` next to `screen_name`) sharing the same underlying connection/wallet -- pick whichever fits your own code."""

    def screen_name(self, request: ScreenNameRequest) -> ScreenNameResponse:
        """Sanctions check: OFAC list check and sanctions screening of a person or company name against OFAC SDN, EU and UN lists (AML KYC) ($0.01, x402)"""
        logger.debug("screen_name: calling %s", "/v1/sanctions-check/screen_name")
        return ScreenNameResponse.model_validate(self._post("/v1/sanctions-check/screen_name", request.model_dump(mode="json", exclude_none=True)))

    async def ascreen_name(self, request: ScreenNameRequest) -> ScreenNameResponse:
        """Sanctions check: OFAC list check and sanctions screening of a person or company name against OFAC SDN, EU and UN lists (AML KYC) ($0.01, x402) (async)"""
        logger.debug("ascreen_name: calling %s", "/v1/sanctions-check/screen_name")
        return ScreenNameResponse.model_validate(await self._apost("/v1/sanctions-check/screen_name", request.model_dump(mode="json", exclude_none=True)))

