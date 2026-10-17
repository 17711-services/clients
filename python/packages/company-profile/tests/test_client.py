"""Verifies every company-profile client method (sync and async) sends a request to the expected path/HTTP verb and parses a well-formed response into the expected type."""

from __future__ import annotations

import asyncio

import httpx

from xyz17711_company_profile import Client
from xyz17711_company_profile.models import *  # noqa: F401,F403


def _mock_client(handler) -> Client:
    """A Client wired to a fake transport for BOTH its sync and async HTTP clients -- no real network call ever happens in this test module. Found live: the async client is normally constructed LAZILY on first async use, so a test that only mocks `_http` (sync) silently lets an async test make a REAL network call instead of using the mock."""
    client = Client("https://example.test")
    client._http = httpx.Client(base_url="https://example.test", transport=httpx.MockTransport(handler))
    client._ahttp = httpx.AsyncClient(base_url="https://example.test", transport=httpx.MockTransport(handler))
    return client


def test_get_profile_calls_the_expected_path():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/v1/company-profile/get_profile"
        return httpx.Response(200, json=GetCompanyProfileResponse._dummy().model_dump(mode='json'))

    client = _mock_client(handler)
    result = client.get_profile(GetCompanyProfileRequest._dummy())
    assert isinstance(result, GetCompanyProfileResponse)


def test_aget_profile_calls_the_expected_path():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/v1/company-profile/get_profile"
        return httpx.Response(200, json=GetCompanyProfileResponse._dummy().model_dump(mode='json'))

    client = _mock_client(handler)

    async def run():
        return await client.aget_profile(GetCompanyProfileRequest._dummy())

    result = asyncio.run(run())
    assert isinstance(result, GetCompanyProfileResponse)

