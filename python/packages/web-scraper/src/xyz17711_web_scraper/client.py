"""Typed HTTP client for web-scraper -- one method per operation, each with a sync form and an async (`a`-prefixed) form."""

from __future__ import annotations

import logging
from typing import Optional

from xyz17711_core import Client as _BaseClient

from .models import *  # noqa: F401,F403 -- re-exported for callers building requests

logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = "https://api.17711.xyz/registry/web-scraper"
"""Production base URL of this service; pass another `base_url` to self-host or test."""


class Client(_BaseClient):
    """Typed client for web-scraper. Every method has a sync form and an async form (the `a`-prefixed sibling, e.g. `aextract_markdown` next to `extract_markdown`) sharing the same underlying connection/wallet -- pick whichever fits your own code."""

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

    def extract_markdown(self, request: ExtractMarkdownRequest) -> ExtractMarkdownResponse:
        """URL to Markdown: read any web page and get its main article content as clean Markdown for agents ($0.003, x402)"""
        logger.debug("extract_markdown: calling %s", "/v1/web-scraper/extract_markdown")
        return ExtractMarkdownResponse.model_validate(self._post("/v1/web-scraper/extract_markdown", request.model_dump(mode="json", exclude_none=True)))

    async def aextract_markdown(self, request: ExtractMarkdownRequest) -> ExtractMarkdownResponse:
        """URL to Markdown: read any web page and get its main article content as clean Markdown for agents ($0.003, x402) (async)"""
        logger.debug("aextract_markdown: calling %s", "/v1/web-scraper/extract_markdown")
        return ExtractMarkdownResponse.model_validate(await self._apost("/v1/web-scraper/extract_markdown", request.model_dump(mode="json", exclude_none=True)))

    def get_task_status(self, request: GetTaskStatusRequest) -> GetTaskStatusResponse:
        """Polls for the result of a task enqueued by a *_async tool"""
        logger.debug("get_task_status: calling %s", "/v1/web-scraper/get_task_status")
        return GetTaskStatusResponse.model_validate(self._post("/v1/web-scraper/get_task_status", request.model_dump(mode="json", exclude_none=True)))

    async def aget_task_status(self, request: GetTaskStatusRequest) -> GetTaskStatusResponse:
        """Polls for the result of a task enqueued by a *_async tool (async)"""
        logger.debug("aget_task_status: calling %s", "/v1/web-scraper/get_task_status")
        return GetTaskStatusResponse.model_validate(await self._apost("/v1/web-scraper/get_task_status", request.model_dump(mode="json", exclude_none=True)))

    def scrape_url(self, request: ScrapeUrlRequest) -> ScrapeUrlResponse:
        """Scrape URL: fetch any web page through a proxy and get its status, content type and raw HTML ($0.002, x402)"""
        logger.debug("scrape_url: calling %s", "/v1/web-scraper/scrape_url")
        return ScrapeUrlResponse.model_validate(self._post("/v1/web-scraper/scrape_url", request.model_dump(mode="json", exclude_none=True)))

    async def ascrape_url(self, request: ScrapeUrlRequest) -> ScrapeUrlResponse:
        """Scrape URL: fetch any web page through a proxy and get its status, content type and raw HTML ($0.002, x402) (async)"""
        logger.debug("ascrape_url: calling %s", "/v1/web-scraper/scrape_url")
        return ScrapeUrlResponse.model_validate(await self._apost("/v1/web-scraper/scrape_url", request.model_dump(mode="json", exclude_none=True)))

    def scrape_url_async(self, request: ScrapeUrlAsyncRequest) -> AsyncTaskResponse:
        """[Deprecated - use web_scraper_scrape_url] Enqueues a web_scraper_scrape_url job and returns a task id immediately ($0.002, x402)"""
        logger.debug("scrape_url_async: calling %s", "/v1/web-scraper/scrape_url_async")
        return AsyncTaskResponse.model_validate(self._post("/v1/web-scraper/scrape_url_async", request.model_dump(mode="json", exclude_none=True)))

    async def ascrape_url_async(self, request: ScrapeUrlAsyncRequest) -> AsyncTaskResponse:
        """[Deprecated - use web_scraper_scrape_url] Enqueues a web_scraper_scrape_url job and returns a task id immediately ($0.002, x402) (async)"""
        logger.debug("ascrape_url_async: calling %s", "/v1/web-scraper/scrape_url_async")
        return AsyncTaskResponse.model_validate(await self._apost("/v1/web-scraper/scrape_url_async", request.model_dump(mode="json", exclude_none=True)))

