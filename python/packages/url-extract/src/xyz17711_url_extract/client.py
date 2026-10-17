"""Typed HTTP client for url-extract-service -- one method per operation, each with a sync form and an async (`a`-prefixed) form."""

from __future__ import annotations

import logging
from typing import Optional

from xyz17711_core import Client as _BaseClient

from .models import *  # noqa: F401,F403 -- re-exported for callers building requests

logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = "https://api.17711.xyz/registry/url-extract-service"
"""Production base URL of this service; pass another `base_url` to self-host or test."""


class Client(_BaseClient):
    """Typed client for url-extract-service. Every method has a sync form and an async form (the `a`-prefixed sibling, e.g. `aget_company_profile` next to `get_company_profile`) sharing the same underlying connection/wallet -- pick whichever fits your own code."""

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

    def get_company_profile(self, request: GetCompanyProfileRequest) -> GetCompanyProfileResponse:
        """[Deprecated - use company_profile_get_profile] Company profile from a domain or a name as valid JSON ($0.009, x402)"""
        logger.debug("get_company_profile: calling %s", "/v1/url-extract/get_company_profile")
        return GetCompanyProfileResponse.model_validate(self._post("/v1/url-extract/get_company_profile", request.model_dump(mode="json", exclude_none=True)))

    async def aget_company_profile(self, request: GetCompanyProfileRequest) -> GetCompanyProfileResponse:
        """[Deprecated - use company_profile_get_profile] Company profile from a domain or a name as valid JSON ($0.009, x402) (async)"""
        logger.debug("aget_company_profile: calling %s", "/v1/url-extract/get_company_profile")
        return GetCompanyProfileResponse.model_validate(await self._apost("/v1/url-extract/get_company_profile", request.model_dump(mode="json", exclude_none=True)))

    def get_structured_data(self, request: GetStructuredDataRequest) -> GetStructuredDataResponse:
        """URL extract with a question: ask any web page a question and get structured data as JSON that matches your schema ($0.02, x402)"""
        logger.debug("get_structured_data: calling %s", "/v1/url-extract/get_structured_data")
        return GetStructuredDataResponse.model_validate(self._post("/v1/url-extract/get_structured_data", request.model_dump(mode="json", exclude_none=True)))

    async def aget_structured_data(self, request: GetStructuredDataRequest) -> GetStructuredDataResponse:
        """URL extract with a question: ask any web page a question and get structured data as JSON that matches your schema ($0.02, x402) (async)"""
        logger.debug("aget_structured_data: calling %s", "/v1/url-extract/get_structured_data")
        return GetStructuredDataResponse.model_validate(await self._apost("/v1/url-extract/get_structured_data", request.model_dump(mode="json", exclude_none=True)))

