"""Verifies every extract-correct LangChain tool through the real StructuredTool (both `.invoke()` and `.ainvoke()`), not just the underlying client method -- catches schema-shape bugs a plain client-method test would miss. Requires the `langchain` extra."""

from __future__ import annotations

import asyncio

import httpx

from xyz17711_extract_correct import Client
from xyz17711_extract_correct.langchain_tools import ExtractCorrectToolkit
from xyz17711_extract_correct.models import *  # noqa: F401,F403


def _mock_client(handler) -> Client:
    client = Client("https://example.test")
    client._http = httpx.Client(base_url="https://example.test", transport=httpx.MockTransport(handler))
    client._ahttp = httpx.AsyncClient(base_url="https://example.test", transport=httpx.MockTransport(handler))
    return client


def test_parse_json_tool_invoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=ParseJsonResponse._dummy().model_dump(mode='json'))

    toolkit = ExtractCorrectToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "parse_json")
    result = tool.invoke({"schema": None, "text": "test"})
    assert result is not None


def test_parse_json_tool_ainvoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=ParseJsonResponse._dummy().model_dump(mode='json'))

    toolkit = ExtractCorrectToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "parse_json")

    async def run():
        return await tool.ainvoke({"schema": None, "text": "test"})

    result = asyncio.run(run())
    assert result is not None

