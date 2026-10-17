"""LangChain `StructuredTool`s for web-scraper, grouped in one `BaseToolkit` -- one tool per operation, each with both a sync and an async implementation. Requires the `langchain` extra: pip install "xyz17711-web-scraper[langchain]"."""

from __future__ import annotations

import logging
from typing import Any, List, Optional

from langchain_core.tools import BaseTool, BaseToolkit, StructuredTool

from .client import Client
from .models import *  # noqa: F401,F403 -- request models reused as tool args_schema

logger = logging.getLogger(__name__)


class WebScraperToolkit(BaseToolkit):
    """LangChain toolkit for web-scraper -- one StructuredTool per operation, reusing this package's own generated client and request models directly. Each tool carries both a sync and an async (`coroutine=`) implementation, so `.invoke()` and `.ainvoke()` both work."""

    client: Client
    model_config = {"arbitrary_types_allowed": True}

    def get_tools(self) -> List[BaseTool]:
        logger.debug("WebScraperToolkit.get_tools: building 4 tool(s)")
        def _extract_markdown(**kwargs: Any) -> Any:
            logger.debug("WebScraperToolkit.get_tools: calling extract_markdown")
            return self.client.extract_markdown(ExtractMarkdownRequest(**kwargs)).model_dump()

        async def _aextract_markdown(**kwargs: Any) -> Any:
            logger.debug("WebScraperToolkit.get_tools: calling extract_markdown (async)")
            return (await self.client.aextract_markdown(ExtractMarkdownRequest(**kwargs))).model_dump()

        def _get_task_status(**kwargs: Any) -> Any:
            logger.debug("WebScraperToolkit.get_tools: calling get_task_status")
            return self.client.get_task_status(GetTaskStatusRequest(**kwargs)).model_dump()

        async def _aget_task_status(**kwargs: Any) -> Any:
            logger.debug("WebScraperToolkit.get_tools: calling get_task_status (async)")
            return (await self.client.aget_task_status(GetTaskStatusRequest(**kwargs))).model_dump()

        def _scrape_url(**kwargs: Any) -> Any:
            logger.debug("WebScraperToolkit.get_tools: calling scrape_url")
            return self.client.scrape_url(ScrapeUrlRequest(**kwargs)).model_dump()

        async def _ascrape_url(**kwargs: Any) -> Any:
            logger.debug("WebScraperToolkit.get_tools: calling scrape_url (async)")
            return (await self.client.ascrape_url(ScrapeUrlRequest(**kwargs))).model_dump()

        def _scrape_url_async(**kwargs: Any) -> Any:
            logger.debug("WebScraperToolkit.get_tools: calling scrape_url_async")
            return self.client.scrape_url_async(ScrapeUrlAsyncRequest(**kwargs)).model_dump()

        async def _ascrape_url_async(**kwargs: Any) -> Any:
            logger.debug("WebScraperToolkit.get_tools: calling scrape_url_async (async)")
            return (await self.client.ascrape_url_async(ScrapeUrlAsyncRequest(**kwargs))).model_dump()

        return [
            StructuredTool.from_function(
                func=_extract_markdown,
                coroutine=_aextract_markdown,
                name="extract_markdown",
                description="URL to Markdown: read any web page and get its main article content as clean Markdown for agents ($0.003, x402)",
                args_schema=ExtractMarkdownRequest,
            ),
            StructuredTool.from_function(
                func=_get_task_status,
                coroutine=_aget_task_status,
                name="get_task_status",
                description="Polls for the result of a task enqueued by a *_async tool",
                args_schema=GetTaskStatusRequest,
            ),
            StructuredTool.from_function(
                func=_scrape_url,
                coroutine=_ascrape_url,
                name="scrape_url",
                description="Scrape URL: fetch any web page through a proxy and get its status, content type and raw HTML ($0.002, x402)",
                args_schema=ScrapeUrlRequest,
            ),
            StructuredTool.from_function(
                func=_scrape_url_async,
                coroutine=_ascrape_url_async,
                name="scrape_url_async",
                description="[Deprecated - use web_scraper_scrape_url] Enqueues a web_scraper_scrape_url job and returns a task id immediately ($0.002, x402)",
                args_schema=ScrapeUrlAsyncRequest,
            ),
        ]
