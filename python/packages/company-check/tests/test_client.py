"""Verifies every company-check client method (sync and async) sends a request to the expected path/HTTP verb and parses a well-formed response into the expected type."""

from __future__ import annotations

import asyncio

import httpx

from xyz17711_company_check import Client
from xyz17711_company_check.models import *  # noqa: F401,F403


def _mock_client(handler) -> Client:
    """A Client wired to a fake transport for BOTH its sync and async HTTP clients -- no real network call ever happens in this test module. Found live: the async client is normally constructed LAZILY on first async use, so a test that only mocks `_http` (sync) silently lets an async test make a REAL network call instead of using the mock."""
    client = Client("https://example.test")
    client._http = httpx.Client(base_url="https://example.test", transport=httpx.MockTransport(handler))
    client._ahttp = httpx.AsyncClient(base_url="https://example.test", transport=httpx.MockTransport(handler))
    return client


def test_verify_company_calls_the_expected_path():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/v1/company-check/verify_company"
        return httpx.Response(200, json=VerifyCompanyResponse._dummy().model_dump(mode='json'))

    client = _mock_client(handler)
    result = client.verify_company(VerifyCompanyRequest._dummy())
    assert isinstance(result, VerifyCompanyResponse)


def test_averify_company_calls_the_expected_path():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/v1/company-check/verify_company"
        return httpx.Response(200, json=VerifyCompanyResponse._dummy().model_dump(mode='json'))

    client = _mock_client(handler)

    async def run():
        return await client.averify_company(VerifyCompanyRequest._dummy())

    result = asyncio.run(run())
    assert isinstance(result, VerifyCompanyResponse)

