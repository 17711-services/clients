"""Verifies every catalog LangChain tool through the real StructuredTool (both `.invoke()` and `.ainvoke()`), not just the underlying client method -- catches schema-shape bugs a plain client-method test would miss. Requires the `langchain` extra."""

from __future__ import annotations

import asyncio

import httpx

from xyz17711_catalog import Client
from xyz17711_catalog.langchain_tools import CatalogToolkit
from xyz17711_catalog.models import *  # noqa: F401,F403


def _mock_client(handler) -> Client:
    client = Client("https://example.test")
    client._http = httpx.Client(base_url="https://example.test", transport=httpx.MockTransport(handler))
    client._ahttp = httpx.AsyncClient(base_url="https://example.test", transport=httpx.MockTransport(handler))
    return client


def test_category_tool_invoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=CatalogCategoryResponse._dummy().model_dump(mode='json'))

    toolkit = CatalogToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "category")
    result = tool.invoke({"q": "test", "limit": None, "offset": None})
    assert result is not None


def test_category_tool_ainvoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=CatalogCategoryResponse._dummy().model_dump(mode='json'))

    toolkit = CatalogToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "category")

    async def run():
        return await tool.ainvoke({"q": "test", "limit": None, "offset": None})

    result = asyncio.run(run())
    assert result is not None


def test_find_services_by_capability_tool_invoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=SearchResponse._dummy().model_dump(mode='json'))

    toolkit = CatalogToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "find_services_by_capability")
    result = tool.invoke({"query": "test", "top_k": None})
    assert result is not None


def test_find_services_by_capability_tool_ainvoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=SearchResponse._dummy().model_dump(mode='json'))

    toolkit = CatalogToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "find_services_by_capability")

    async def run():
        return await tool.ainvoke({"query": "test", "top_k": None})

    result = asyncio.run(run())
    assert result is not None


def test_search_tool_invoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=CatalogSearchResponse._dummy().model_dump(mode='json'))

    toolkit = CatalogToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "search")
    result = tool.invoke({"q": "test", "category": None, "limit": None})
    assert result is not None


def test_search_tool_ainvoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=CatalogSearchResponse._dummy().model_dump(mode='json'))

    toolkit = CatalogToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "search")

    async def run():
        return await tool.ainvoke({"q": "test", "category": None, "limit": None})

    result = asyncio.run(run())
    assert result is not None

