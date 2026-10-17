"""Typed HTTP client for company-profile-service -- one method per operation, each with a sync form and an async (`a`-prefixed) form."""

from __future__ import annotations

import logging

from xyz17711_core import Client as _BaseClient

from .models import *  # noqa: F401,F403 -- re-exported for callers building requests

logger = logging.getLogger(__name__)


class Client(_BaseClient):
    """Typed client for company-profile-service. Every method has a sync form and an async form (the `a`-prefixed sibling, e.g. `aget_profile` next to `get_profile`) sharing the same underlying connection/wallet -- pick whichever fits your own code."""

    def get_profile(self, request: GetCompanyProfileRequest) -> GetCompanyProfileResponse:
        """Company profile and enrichment from a domain or a name: offering, public contacts, social links and WHOIS domain data as valid JSON ($0.009, x402)"""
        logger.debug("get_profile: calling %s", "/v1/company-profile/get_profile")
        return GetCompanyProfileResponse.model_validate(self._post("/v1/company-profile/get_profile", request.model_dump(mode="json", exclude_none=True)))

    async def aget_profile(self, request: GetCompanyProfileRequest) -> GetCompanyProfileResponse:
        """Company profile and enrichment from a domain or a name: offering, public contacts, social links and WHOIS domain data as valid JSON ($0.009, x402) (async)"""
        logger.debug("aget_profile: calling %s", "/v1/company-profile/get_profile")
        return GetCompanyProfileResponse.model_validate(await self._apost("/v1/company-profile/get_profile", request.model_dump(mode="json", exclude_none=True)))

