"""Verifies every websearch LangChain tool through the real StructuredTool (both `.invoke()` and `.ainvoke()`), not just the underlying client method -- catches schema-shape bugs a plain client-method test would miss. Requires the `langchain` extra."""

from __future__ import annotations

import asyncio

import httpx

from xyz17711_websearch import Client
from xyz17711_websearch.langchain_tools import WebsearchToolkit
from xyz17711_websearch.models import *  # noqa: F401,F403


def _mock_client(handler) -> Client:
    client = Client("https://example.test")
    client._http = httpx.Client(base_url="https://example.test", transport=httpx.MockTransport(handler))
    client._ahttp = httpx.AsyncClient(base_url="https://example.test", transport=httpx.MockTransport(handler))
    return client


def test_get_task_status_tool_invoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=GetTaskStatusResponse._dummy().model_dump(mode='json'))

    toolkit = WebsearchToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "get_task_status")
    result = tool.invoke({"task_id": "test"})
    assert result is not None


def test_get_task_status_tool_ainvoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=GetTaskStatusResponse._dummy().model_dump(mode='json'))

    toolkit = WebsearchToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "get_task_status")

    async def run():
        return await tool.ainvoke({"task_id": "test"})

    result = asyncio.run(run())
    assert result is not None


def test_search_web_tool_invoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=SearchWebResponse._dummy().model_dump(mode='json'))

    toolkit = WebsearchToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "search_web")
    result = tool.invoke({"query": "test"})
    assert result is not None


def test_search_web_tool_ainvoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=SearchWebResponse._dummy().model_dump(mode='json'))

    toolkit = WebsearchToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "search_web")

    async def run():
        return await tool.ainvoke({"query": "test"})

    result = asyncio.run(run())
    assert result is not None


def test_search_web_async_tool_invoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=AsyncTaskResponse._dummy().model_dump(mode='json'))

    toolkit = WebsearchToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "search_web_async")
    result = tool.invoke({"callback_url": None, "query": "test"})
    assert result is not None


def test_search_web_async_tool_ainvoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=AsyncTaskResponse._dummy().model_dump(mode='json'))

    toolkit = WebsearchToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "search_web_async")

    async def run():
        return await tool.ainvoke({"callback_url": None, "query": "test"})

    result = asyncio.run(run())
    assert result is not None

