"""LangChain `StructuredTool`s for company-check-service, grouped in one `BaseToolkit` -- one tool per operation, each with both a sync and an async implementation. Requires the `langchain` extra: pip install "xyz17711-company-check[langchain]"."""

from __future__ import annotations

import logging
from typing import Any, List, Optional

from langchain_core.tools import BaseTool, BaseToolkit, StructuredTool

from .client import Client
from .models import *  # noqa: F401,F403 -- request models reused as tool args_schema

logger = logging.getLogger(__name__)


class CompanyCheckToolkit(BaseToolkit):
    """LangChain toolkit for company-check-service -- one StructuredTool per operation, reusing this package's own generated client and request models directly. Each tool carries both a sync and an async (`coroutine=`) implementation, so `.invoke()` and `.ainvoke()` both work."""

    client: Client
    model_config = {"arbitrary_types_allowed": True}

    def get_tools(self) -> List[BaseTool]:
        logger.debug("CompanyCheckToolkit.get_tools: building 1 tool(s)")
        def _verify_company(**kwargs: Any) -> Any:
            logger.debug("CompanyCheckToolkit.get_tools: calling verify_company")
            return self.client.verify_company(VerifyCompanyRequest(**kwargs)).model_dump()

        async def _averify_company(**kwargs: Any) -> Any:
            logger.debug("CompanyCheckToolkit.get_tools: calling verify_company (async)")
            return (await self.client.averify_company(VerifyCompanyRequest(**kwargs))).model_dump()

        return [
            StructuredTool.from_function(
                func=_verify_company,
                coroutine=_averify_company,
                name="verify_company",
                description="Company check (KYB) and business verification: VAT validation (VIES), LEI lookup, registry status and company directors ($0.009, x402)",
                args_schema=VerifyCompanyRequest,
            ),
        ]
