"""Verifies every emoji-match LangChain tool through the real StructuredTool (both `.invoke()` and `.ainvoke()`), not just the underlying client method -- catches schema-shape bugs a plain client-method test would miss. Requires the `langchain` extra."""

from __future__ import annotations

import asyncio

import httpx

from xyz17711_emoji_match import Client
from xyz17711_emoji_match.langchain_tools import EmojiMatchToolkit
from xyz17711_emoji_match.models import *  # noqa: F401,F403


def _mock_client(handler) -> Client:
    client = Client("https://example.test")
    client._http = httpx.Client(base_url="https://example.test", transport=httpx.MockTransport(handler))
    client._ahttp = httpx.AsyncClient(base_url="https://example.test", transport=httpx.MockTransport(handler))
    return client


def test_suggest_emojis_tool_invoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=SuggestEmojisResponse._dummy().model_dump(mode='json'))

    toolkit = EmojiMatchToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "suggest_emojis")
    result = tool.invoke({"text": "test"})
    assert result is not None


def test_suggest_emojis_tool_ainvoke():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=SuggestEmojisResponse._dummy().model_dump(mode='json'))

    toolkit = EmojiMatchToolkit(client=_mock_client(handler))
    tool = next(t for t in toolkit.get_tools() if t.name == "suggest_emojis")

    async def run():
        return await tool.ainvoke({"text": "test"})

    result = asyncio.run(run())
    assert result is not None

