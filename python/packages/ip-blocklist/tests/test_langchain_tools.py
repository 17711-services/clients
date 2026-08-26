"""Verifies every ip-blocklist LangChain tool through the real StructuredTool (both `.invoke()` and `.ainvoke()`), not just the underlying client method -- catches schema-shape bugs a plain client-method test would miss. Requires the `langchain` extra."""

from __future__ import annotations

import asyncio

import httpx

from xyz17711_ip_blocklist import Client
from xyz17711_ip_blocklist.langchain_tools import IpBlocklistToolkit
from xyz17711_ip_blocklist.models import *  # noqa: F401,F403


def _mock_client(handler) -> Client:
    client = Client("https://example.test")
    client._http = httpx.Client(base_url="https://example.test", transport=httpx.MockTransport(handler))
    client._ahttp = httpx.AsyncClient(base_url="https://example.test", transport=httpx.MockTransport(handler))
    return client


def test_check_ip_tool_invoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=CheckIpResponse._dummy().model_dump(mode='json'))

    toolkit = IpBlocklistToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "check_ip")
    result = tool.invoke({"ip": "test"})
    assert result is not None


def test_check_ip_tool_ainvoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=CheckIpResponse._dummy().model_dump(mode='json'))

    toolkit = IpBlocklistToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "check_ip")

    async def run():
        return await tool.ainvoke({"ip": "test"})

    result = asyncio.run(run())
    assert result is not None

