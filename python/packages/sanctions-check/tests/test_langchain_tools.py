"""Verifies every sanctions-check LangChain tool through the real StructuredTool (both `.invoke()` and `.ainvoke()`), not just the underlying client method -- catches schema-shape bugs a plain client-method test would miss. Requires the `langchain` extra."""

from __future__ import annotations

import asyncio

import httpx

from xyz17711_sanctions_check import Client
from xyz17711_sanctions_check.langchain_tools import SanctionsCheckToolkit
from xyz17711_sanctions_check.models import *  # noqa: F401,F403


def _mock_client(handler) -> Client:
    client = Client("https://example.test")
    client._http = httpx.Client(base_url="https://example.test", transport=httpx.MockTransport(handler))
    client._ahttp = httpx.AsyncClient(base_url="https://example.test", transport=httpx.MockTransport(handler))
    return client


def test_screen_name_tool_invoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=ScreenNameResponse._dummy().model_dump(mode='json'))

    toolkit = SanctionsCheckToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "screen_name")
    result = tool.invoke({"birth_year": None, "name": "test", "type": None})
    assert result is not None


def test_screen_name_tool_ainvoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=ScreenNameResponse._dummy().model_dump(mode='json'))

    toolkit = SanctionsCheckToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "screen_name")

    async def run():
        return await tool.ainvoke({"birth_year": None, "name": "test", "type": None})

    result = asyncio.run(run())
    assert result is not None

