"""LangChain `StructuredTool`s for proxy-pool, grouped in one `BaseToolkit` -- one tool per operation, each with both a sync and an async implementation. Requires the `langchain` extra: pip install "xyz17711-proxy-pool[langchain]"."""

from __future__ import annotations

import logging
from typing import Any, List, Optional

from langchain_core.tools import BaseTool, BaseToolkit, StructuredTool

from .client import Client
from .models import *  # noqa: F401,F403 -- request models reused as tool args_schema

logger = logging.getLogger(__name__)


class ProxyPoolToolkit(BaseToolkit):
    """LangChain toolkit for proxy-pool -- one StructuredTool per operation, reusing this package's own generated client and request models directly. Each tool carries both a sync and an async (`coroutine=`) implementation, so `.invoke()` and `.ainvoke()` both work."""

    client: Client
    model_config = {"arbitrary_types_allowed": True}

    def get_tools(self) -> List[BaseTool]:
        logger.debug("ProxyPoolToolkit.get_tools: building 1 tool(s)")
        def _get_best_proxy(anonymity: Optional[str] = None, city: Optional[str] = None, country: Optional[str] = None, protocol: Optional[str] = None) -> Any:
            logger.debug("ProxyPoolToolkit.get_tools: calling get_best_proxy")
            return self.client.get_best_proxy(anonymity=anonymity, city=city, country=country, protocol=protocol).model_dump()

        async def _aget_best_proxy(anonymity: Optional[str] = None, city: Optional[str] = None, country: Optional[str] = None, protocol: Optional[str] = None) -> Any:
            logger.debug("ProxyPoolToolkit.get_tools: calling get_best_proxy (async)")
            return (await self.client.aget_best_proxy(anonymity=anonymity, city=city, country=country, protocol=protocol)).model_dump()

        return [
            StructuredTool.from_function(
                func=_get_best_proxy,
                coroutine=_aget_best_proxy,
                name="get_best_proxy",
                description="Free proxy API: get one fast, verified-alive proxy (HTTP, SOCKS) filtered by country, protocol and anonymity, for scraping ($0.010, x402)",
            ),
        ]
