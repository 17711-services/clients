"""Verifies every web-scraper client method (sync and async) sends a request to the expected path/HTTP verb and parses a well-formed response into the expected type."""

from __future__ import annotations

import asyncio

import httpx

from xyz17711_web_scraper import Client
from xyz17711_web_scraper.models import *  # noqa: F401,F403


def _mock_client(handler) -> Client:
    """A Client wired to a fake transport for BOTH its sync and async HTTP clients -- no real network call ever happens in this test module. Found live: the async client is normally constructed LAZILY on first async use, so a test that only mocks `_http` (sync) silently lets an async test make a REAL network call instead of using the mock."""
    client = Client("https://example.test")
    client._http = httpx.Client(base_url="https://example.test", transport=httpx.MockTransport(handler))
    client._ahttp = httpx.AsyncClient(base_url="https://example.test", transport=httpx.MockTransport(handler))
    return client


def test_extract_markdown_calls_the_expected_path():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/v1/web-scraper/extract_markdown"
        return httpx.Response(200, json=ExtractMarkdownResponse._dummy().model_dump(mode='json'))

    client = _mock_client(handler)
    result = client.extract_markdown(ExtractMarkdownRequest._dummy())
    assert isinstance(result, ExtractMarkdownResponse)


def test_aextract_markdown_calls_the_expected_path():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/v1/web-scraper/extract_markdown"
        return httpx.Response(200, json=ExtractMarkdownResponse._dummy().model_dump(mode='json'))

    client = _mock_client(handler)

    async def run():
        return await client.aextract_markdown(ExtractMarkdownRequest._dummy())

    result = asyncio.run(run())
    assert isinstance(result, ExtractMarkdownResponse)


def test_get_task_status_calls_the_expected_path():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/v1/web-scraper/get_task_status"
        return httpx.Response(200, json=GetTaskStatusResponse._dummy().model_dump(mode='json'))

    client = _mock_client(handler)
    result = client.get_task_status(GetTaskStatusRequest._dummy())
    assert isinstance(result, GetTaskStatusResponse)


def test_aget_task_status_calls_the_expected_path():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/v1/web-scraper/get_task_status"
        return httpx.Response(200, json=GetTaskStatusResponse._dummy().model_dump(mode='json'))

    client = _mock_client(handler)

    async def run():
        return await client.aget_task_status(GetTaskStatusRequest._dummy())

    result = asyncio.run(run())
    assert isinstance(result, GetTaskStatusResponse)


def test_scrape_url_calls_the_expected_path():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/v1/web-scraper/scrape_url"
        return httpx.Response(200, json=ScrapeUrlResponse._dummy().model_dump(mode='json'))

    client = _mock_client(handler)
    result = client.scrape_url(ScrapeUrlRequest._dummy())
    assert isinstance(result, ScrapeUrlResponse)


def test_ascrape_url_calls_the_expected_path():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/v1/web-scraper/scrape_url"
        return httpx.Response(200, json=ScrapeUrlResponse._dummy().model_dump(mode='json'))

    client = _mock_client(handler)

    async def run():
        return await client.ascrape_url(ScrapeUrlRequest._dummy())

    result = asyncio.run(run())
    assert isinstance(result, ScrapeUrlResponse)


def test_scrape_url_async_calls_the_expected_path():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/v1/web-scraper/scrape_url_async"
        return httpx.Response(200, json=AsyncTaskResponse._dummy().model_dump(mode='json'))

    client = _mock_client(handler)
    result = client.scrape_url_async(ScrapeUrlAsyncRequest._dummy())
    assert isinstance(result, AsyncTaskResponse)


def test_ascrape_url_async_calls_the_expected_path():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/v1/web-scraper/scrape_url_async"
        return httpx.Response(200, json=AsyncTaskResponse._dummy().model_dump(mode='json'))

    client = _mock_client(handler)

    async def run():
        return await client.ascrape_url_async(ScrapeUrlAsyncRequest._dummy())

    result = asyncio.run(run())
    assert isinstance(result, AsyncTaskResponse)

