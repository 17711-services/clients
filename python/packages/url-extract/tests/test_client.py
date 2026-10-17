"""Verifies every url-extract client method (sync and async) sends a request to the expected path/HTTP verb and parses a well-formed response into the expected type."""

from __future__ import annotations

import asyncio

import httpx

from xyz17711_url_extract import Client
from xyz17711_url_extract.models import *  # noqa: F401,F403


def _mock_client(handler) -> Client:
    """A Client wired to a fake transport for BOTH its sync and async HTTP clients -- no real network call ever happens in this test module. Found live: the async client is normally constructed LAZILY on first async use, so a test that only mocks `_http` (sync) silently lets an async test make a REAL network call instead of using the mock."""
    client = Client("https://example.test")
    client._http = httpx.Client(base_url="https://example.test", transport=httpx.MockTransport(handler))
    client._ahttp = httpx.AsyncClient(base_url="https://example.test", transport=httpx.MockTransport(handler))
    return client


def test_get_company_profile_calls_the_expected_path():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/v1/url-extract/get_company_profile"
        return httpx.Response(200, json=GetCompanyProfileResponse._dummy().model_dump(mode='json'))

    client = _mock_client(handler)
    result = client.get_company_profile(GetCompanyProfileRequest._dummy())
    assert isinstance(result, GetCompanyProfileResponse)


def test_aget_company_profile_calls_the_expected_path():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/v1/url-extract/get_company_profile"
        return httpx.Response(200, json=GetCompanyProfileResponse._dummy().model_dump(mode='json'))

    client = _mock_client(handler)

    async def run():
        return await client.aget_company_profile(GetCompanyProfileRequest._dummy())

    result = asyncio.run(run())
    assert isinstance(result, GetCompanyProfileResponse)


def test_get_structured_data_calls_the_expected_path():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/v1/url-extract/get_structured_data"
        return httpx.Response(200, json=GetStructuredDataResponse._dummy().model_dump(mode='json'))

    client = _mock_client(handler)
    result = client.get_structured_data(GetStructuredDataRequest._dummy())
    assert isinstance(result, GetStructuredDataResponse)


def test_aget_structured_data_calls_the_expected_path():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/v1/url-extract/get_structured_data"
        return httpx.Response(200, json=GetStructuredDataResponse._dummy().model_dump(mode='json'))

    client = _mock_client(handler)

    async def run():
        return await client.aget_structured_data(GetStructuredDataRequest._dummy())

    result = asyncio.run(run())
    assert isinstance(result, GetStructuredDataResponse)

