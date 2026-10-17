"""LangChain `StructuredTool`s for 🛡️ domain-security-service, grouped in one `BaseToolkit` -- one tool per operation, each with both a sync and an async implementation. Requires the `langchain` extra: pip install "xyz17711-domain-security[langchain]"."""

from __future__ import annotations

import logging
from typing import Any, List, Optional

from langchain_core.tools import BaseTool, BaseToolkit, StructuredTool

from .client import Client
from .models import *  # noqa: F401,F403 -- request models reused as tool args_schema

logger = logging.getLogger(__name__)


class DomainSecurityToolkit(BaseToolkit):
    """LangChain toolkit for 🛡️ domain-security-service -- one StructuredTool per operation, reusing this package's own generated client and request models directly. Each tool carries both a sync and an async (`coroutine=`) implementation, so `.invoke()` and `.ainvoke()` both work."""

    client: Client
    model_config = {"arbitrary_types_allowed": True}

    def get_tools(self) -> List[BaseTool]:
        logger.debug("DomainSecurityToolkit.get_tools: building 1 tool(s)")
        def _get_report(**kwargs: Any) -> Any:
            logger.debug("DomainSecurityToolkit.get_tools: calling get_report")
            return self.client.get_report(GetReportRequest(**kwargs)).model_dump()

        async def _aget_report(**kwargs: Any) -> Any:
            logger.debug("DomainSecurityToolkit.get_tools: calling get_report (async)")
            return (await self.client.aget_report(GetReportRequest(**kwargs))).model_dump()

        return [
            StructuredTool.from_function(
                func=_get_report,
                coroutine=_aget_report,
                name="get_report",
                description="Domain security check: SSL certificate check, DMARC SPF check, DNSSEC, security headers and blocklist status with a score ($0.009, x402)",
                args_schema=GetReportRequest,
            ),
        ]
