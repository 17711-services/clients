"""Verifies every web-scraper LangChain tool through the real StructuredTool (both `.invoke()` and `.ainvoke()`), not just the underlying client method -- catches schema-shape bugs a plain client-method test would miss. Requires the `langchain` extra."""

from __future__ import annotations

import asyncio

import httpx

from xyz17711_web_scraper import Client
from xyz17711_web_scraper.langchain_tools import WebScraperToolkit
from xyz17711_web_scraper.models import *  # noqa: F401,F403


def _mock_client(handler) -> Client:
    client = Client("https://example.test")
    client._http = httpx.Client(base_url="https://example.test", transport=httpx.MockTransport(handler))
    client._ahttp = httpx.AsyncClient(base_url="https://example.test", transport=httpx.MockTransport(handler))
    return client


def test_extract_markdown_tool_invoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=ExtractMarkdownResponse._dummy().model_dump(mode='json'))

    toolkit = WebScraperToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "extract_markdown")
    result = tool.invoke({"url": "test"})
    assert result is not None


def test_extract_markdown_tool_ainvoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=ExtractMarkdownResponse._dummy().model_dump(mode='json'))

    toolkit = WebScraperToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "extract_markdown")

    async def run():
        return await tool.ainvoke({"url": "test"})

    result = asyncio.run(run())
    assert result is not None


def test_get_task_status_tool_invoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=GetTaskStatusResponse._dummy().model_dump(mode='json'))

    toolkit = WebScraperToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "get_task_status")
    result = tool.invoke({"task_id": "test"})
    assert result is not None


def test_get_task_status_tool_ainvoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=GetTaskStatusResponse._dummy().model_dump(mode='json'))

    toolkit = WebScraperToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "get_task_status")

    async def run():
        return await tool.ainvoke({"task_id": "test"})

    result = asyncio.run(run())
    assert result is not None


def test_scrape_url_tool_invoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=ScrapeUrlResponse._dummy().model_dump(mode='json'))

    toolkit = WebScraperToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "scrape_url")
    result = tool.invoke({"url": "test"})
    assert result is not None


def test_scrape_url_tool_ainvoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=ScrapeUrlResponse._dummy().model_dump(mode='json'))

    toolkit = WebScraperToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "scrape_url")

    async def run():
        return await tool.ainvoke({"url": "test"})

    result = asyncio.run(run())
    assert result is not None


def test_scrape_url_async_tool_invoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=AsyncTaskResponse._dummy().model_dump(mode='json'))

    toolkit = WebScraperToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "scrape_url_async")
    result = tool.invoke({"callback_url": None, "url": "test"})
    assert result is not None


def test_scrape_url_async_tool_ainvoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=AsyncTaskResponse._dummy().model_dump(mode='json'))

    toolkit = WebScraperToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "scrape_url_async")

    async def run():
        return await tool.ainvoke({"callback_url": None, "url": "test"})

    result = asyncio.run(run())
    assert result is not None

