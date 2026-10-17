"""Verifies every url-extract LangChain tool through the real StructuredTool (both `.invoke()` and `.ainvoke()`), not just the underlying client method -- catches schema-shape bugs a plain client-method test would miss. Requires the `langchain` extra."""

from __future__ import annotations

import asyncio

import httpx

from xyz17711_url_extract import Client
from xyz17711_url_extract.langchain_tools import UrlExtractToolkit
from xyz17711_url_extract.models import *  # noqa: F401,F403


def _mock_client(handler) -> Client:
    client = Client("https://example.test")
    client._http = httpx.Client(base_url="https://example.test", transport=httpx.MockTransport(handler))
    client._ahttp = httpx.AsyncClient(base_url="https://example.test", transport=httpx.MockTransport(handler))
    return client


def test_get_company_profile_tool_invoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=GetCompanyProfileResponse._dummy().model_dump(mode='json'))

    toolkit = UrlExtractToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "get_company_profile")
    result = tool.invoke({"company_name": None, "domain": None, "language": None})
    assert result is not None


def test_get_company_profile_tool_ainvoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=GetCompanyProfileResponse._dummy().model_dump(mode='json'))

    toolkit = UrlExtractToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "get_company_profile")

    async def run():
        return await tool.ainvoke({"company_name": None, "domain": None, "language": None})

    result = asyncio.run(run())
    assert result is not None


def test_get_structured_data_tool_invoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=GetStructuredDataResponse._dummy().model_dump(mode='json'))

    toolkit = UrlExtractToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "get_structured_data")
    result = tool.invoke({"max_age_seconds": None, "question": "test", "schema": None, "url": "test"})
    assert result is not None


def test_get_structured_data_tool_ainvoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=GetStructuredDataResponse._dummy().model_dump(mode='json'))

    toolkit = UrlExtractToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "get_structured_data")

    async def run():
        return await tool.ainvoke({"max_age_seconds": None, "question": "test", "schema": None, "url": "test"})

    result = asyncio.run(run())
    assert result is not None

