"""LangChain `StructuredTool`s for company-profile-service, grouped in one `BaseToolkit` -- one tool per operation, each with both a sync and an async implementation. Requires the `langchain` extra: pip install "xyz17711-company-profile[langchain]"."""

from __future__ import annotations

import logging
from typing import Any, List, Optional

from langchain_core.tools import BaseTool, BaseToolkit, StructuredTool

from .client import Client
from .models import *  # noqa: F401,F403 -- request models reused as tool args_schema

logger = logging.getLogger(__name__)


class CompanyProfileToolkit(BaseToolkit):
    """LangChain toolkit for company-profile-service -- one StructuredTool per operation, reusing this package's own generated client and request models directly. Each tool carries both a sync and an async (`coroutine=`) implementation, so `.invoke()` and `.ainvoke()` both work."""

    client: Client
    model_config = {"arbitrary_types_allowed": True}

    def get_tools(self) -> List[BaseTool]:
        logger.debug("CompanyProfileToolkit.get_tools: building 1 tool(s)")
        def _get_profile(**kwargs: Any) -> Any:
            logger.debug("CompanyProfileToolkit.get_tools: calling get_profile")
            return self.client.get_profile(GetCompanyProfileRequest(**kwargs)).model_dump()

        async def _aget_profile(**kwargs: Any) -> Any:
            logger.debug("CompanyProfileToolkit.get_tools: calling get_profile (async)")
            return (await self.client.aget_profile(GetCompanyProfileRequest(**kwargs))).model_dump()

        return [
            StructuredTool.from_function(
                func=_get_profile,
                coroutine=_aget_profile,
                name="get_profile",
                description="Company profile and enrichment from a domain or a name: offering, public contacts, social links and WHOIS domain data as valid JSON ($0.009, x402)",
                args_schema=GetCompanyProfileRequest,
            ),
        ]
