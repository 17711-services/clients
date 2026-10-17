"""LangChain `StructuredTool`s for 🧩 url-extract-service, grouped in one `BaseToolkit` -- one tool per operation, each with both a sync and an async implementation. Requires the `langchain` extra: pip install "xyz17711-url-extract[langchain]"."""

from __future__ import annotations

import logging
from typing import Any, List, Optional

from langchain_core.tools import BaseTool, BaseToolkit, StructuredTool

from .client import Client
from .models import *  # noqa: F401,F403 -- request models reused as tool args_schema

logger = logging.getLogger(__name__)


class UrlExtractToolkit(BaseToolkit):
    """LangChain toolkit for 🧩 url-extract-service -- one StructuredTool per operation, reusing this package's own generated client and request models directly. Each tool carries both a sync and an async (`coroutine=`) implementation, so `.invoke()` and `.ainvoke()` both work."""

    client: Client
    model_config = {"arbitrary_types_allowed": True}

    def get_tools(self) -> List[BaseTool]:
        logger.debug("UrlExtractToolkit.get_tools: building 2 tool(s)")
        def _get_company_profile(**kwargs: Any) -> Any:
            logger.debug("UrlExtractToolkit.get_tools: calling get_company_profile")
            return self.client.get_company_profile(GetCompanyProfileRequest(**kwargs)).model_dump()

        async def _aget_company_profile(**kwargs: Any) -> Any:
            logger.debug("UrlExtractToolkit.get_tools: calling get_company_profile (async)")
            return (await self.client.aget_company_profile(GetCompanyProfileRequest(**kwargs))).model_dump()

        def _get_structured_data(**kwargs: Any) -> Any:
            logger.debug("UrlExtractToolkit.get_tools: calling get_structured_data")
            return self.client.get_structured_data(GetStructuredDataRequest(**kwargs)).model_dump()

        async def _aget_structured_data(**kwargs: Any) -> Any:
            logger.debug("UrlExtractToolkit.get_tools: calling get_structured_data (async)")
            return (await self.client.aget_structured_data(GetStructuredDataRequest(**kwargs))).model_dump()

        return [
            StructuredTool.from_function(
                func=_get_company_profile,
                coroutine=_aget_company_profile,
                name="get_company_profile",
                description="[Deprecated - use company_profile_get_profile] Company profile from a domain or a name as valid JSON ($0.009, x402)",
                args_schema=GetCompanyProfileRequest,
            ),
            StructuredTool.from_function(
                func=_get_structured_data,
                coroutine=_aget_structured_data,
                name="get_structured_data",
                description="URL extract with a question: ask any web page a question and get structured data as JSON that matches your schema ($0.02, x402)",
                args_schema=GetStructuredDataRequest,
            ),
        ]
