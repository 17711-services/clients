"""Verifies every address-risk LangChain tool through the real StructuredTool (both `.invoke()` and `.ainvoke()`), not just the underlying client method -- catches schema-shape bugs a plain client-method test would miss. Requires the `langchain` extra."""

from __future__ import annotations

import asyncio

import httpx

from xyz17711_address_risk import Client
from xyz17711_address_risk.langchain_tools import AddressRiskToolkit
from xyz17711_address_risk.models import *  # noqa: F401,F403


def _mock_client(handler) -> Client:
    client = Client("https://example.test")
    client._http = httpx.Client(base_url="https://example.test", transport=httpx.MockTransport(handler))
    client._ahttp = httpx.AsyncClient(base_url="https://example.test", transport=httpx.MockTransport(handler))
    return client


def test_check_address_tool_invoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=CheckAddressResponse._dummy().model_dump(mode='json'))

    toolkit = AddressRiskToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "check_address")
    result = tool.invoke({"address": "test", "chain": None, "max_age_seconds": None})
    assert result is not None


def test_check_address_tool_ainvoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=CheckAddressResponse._dummy().model_dump(mode='json'))

    toolkit = AddressRiskToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "check_address")

    async def run():
        return await tool.ainvoke({"address": "test", "chain": None, "max_age_seconds": None})

    result = asyncio.run(run())
    assert result is not None

