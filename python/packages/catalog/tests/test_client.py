"""Verifies every catalog client method (sync and async) sends a request to the expected path/HTTP verb and parses a well-formed response into the expected type."""

from __future__ import annotations

import asyncio

import httpx

from xyz17711_catalog import Client
from xyz17711_catalog.models import *  # noqa: F401,F403


def _mock_client(handler) -> Client:
    """A Client wired to a fake transport for BOTH its sync and async HTTP clients -- no real network call ever happens in this test module. Found live: the async client is normally constructed LAZILY on first async use, so a test that only mocks `_http` (sync) silently lets an async test make a REAL network call instead of using the mock."""
    client = Client("https://example.test")
    client._http = httpx.Client(base_url="https://example.test", transport=httpx.MockTransport(handler))
    client._ahttp = httpx.AsyncClient(base_url="https://example.test", transport=httpx.MockTransport(handler))
    return client


def test_category_calls_the_expected_path():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/v1/catalog/category"
        return httpx.Response(200, json=CatalogCategoryResponse._dummy().model_dump(mode='json'))

    client = _mock_client(handler)
    result = client.category(q="test", limit=None, offset=None)
    assert isinstance(result, CatalogCategoryResponse)


def test_acategory_calls_the_expected_path():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/v1/catalog/category"
        return httpx.Response(200, json=CatalogCategoryResponse._dummy().model_dump(mode='json'))

    client = _mock_client(handler)

    async def run():
        return await client.acategory(q="test", limit=None, offset=None)

    result = asyncio.run(run())
    assert isinstance(result, CatalogCategoryResponse)


def test_find_services_by_capability_calls_the_expected_path():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/v1/catalog/find_services_by_capability"
        return httpx.Response(200, json=SearchResponse._dummy().model_dump(mode='json'))

    client = _mock_client(handler)
    result = client.find_services_by_capability(SearchRequest._dummy())
    assert isinstance(result, SearchResponse)


def test_afind_services_by_capability_calls_the_expected_path():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/v1/catalog/find_services_by_capability"
        return httpx.Response(200, json=SearchResponse._dummy().model_dump(mode='json'))

    client = _mock_client(handler)

    async def run():
        return await client.afind_services_by_capability(SearchRequest._dummy())

    result = asyncio.run(run())
    assert isinstance(result, SearchResponse)


def test_search_calls_the_expected_path():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/v1/catalog/search"
        return httpx.Response(200, json=CatalogSearchResponse._dummy().model_dump(mode='json'))

    client = _mock_client(handler)
    result = client.search(q="test", category=None, limit=None)
    assert isinstance(result, CatalogSearchResponse)


def test_asearch_calls_the_expected_path():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/v1/catalog/search"
        return httpx.Response(200, json=CatalogSearchResponse._dummy().model_dump(mode='json'))

    client = _mock_client(handler)

    async def run():
        return await client.asearch(q="test", category=None, limit=None)

    result = asyncio.run(run())
    assert isinstance(result, CatalogSearchResponse)

