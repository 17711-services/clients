"""Typed HTTP client for company-check-service -- one method per operation, each with a sync form and an async (`a`-prefixed) form."""

from __future__ import annotations

import logging
from typing import Optional

from xyz17711_core import Client as _BaseClient

from .models import *  # noqa: F401,F403 -- re-exported for callers building requests

logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = "https://api.17711.xyz/registry/company-check-service"
"""Production base URL of this service; pass another `base_url` to self-host or test."""


class Client(_BaseClient):
    """Typed client for company-check-service. Every method has a sync form and an async form (the `a`-prefixed sibling, e.g. `averify_company` next to `verify_company`) sharing the same underlying connection/wallet -- pick whichever fits your own code."""

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

    def verify_company(self, request: VerifyCompanyRequest) -> VerifyCompanyResponse:
        """Company check (KYB) and business verification: VAT validation (VIES), LEI lookup, registry status and company directors ($0.009, x402)"""
        logger.debug("verify_company: calling %s", "/v1/company-check/verify_company")
        return VerifyCompanyResponse.model_validate(self._post("/v1/company-check/verify_company", request.model_dump(mode="json", exclude_none=True)))

    async def averify_company(self, request: VerifyCompanyRequest) -> VerifyCompanyResponse:
        """Company check (KYB) and business verification: VAT validation (VIES), LEI lookup, registry status and company directors ($0.009, x402) (async)"""
        logger.debug("averify_company: calling %s", "/v1/company-check/verify_company")
        return VerifyCompanyResponse.model_validate(await self._apost("/v1/company-check/verify_company", request.model_dump(mode="json", exclude_none=True)))

