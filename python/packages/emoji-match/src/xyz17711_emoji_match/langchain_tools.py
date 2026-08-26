"""LangChain `StructuredTool`s for emoji-match-service, grouped in one `BaseToolkit` -- one tool per operation, each with both a sync and an async implementation. Requires the `langchain` extra: pip install "xyz17711-emoji-match[langchain]"."""

from __future__ import annotations

import logging
from typing import Any, List, Optional

from langchain_core.tools import BaseTool, BaseToolkit, StructuredTool

from .client import Client
from .models import *  # noqa: F401,F403 -- request models reused as tool args_schema

logger = logging.getLogger(__name__)


class EmojiMatchToolkit(BaseToolkit):
    """LangChain toolkit for emoji-match-service -- one StructuredTool per operation, reusing this package's own generated client and request models directly. Each tool carries both a sync and an async (`coroutine=`) implementation, so `.invoke()` and `.ainvoke()` both work."""

    client: Client
    model_config = {"arbitrary_types_allowed": True}

    def get_tools(self) -> List[BaseTool]:
        logger.debug("EmojiMatchToolkit.get_tools: building 1 tool(s)")
        def _suggest_emojis(**kwargs: Any) -> Any:
            logger.debug("EmojiMatchToolkit.get_tools: calling suggest_emojis")
            return self.client.suggest_emojis(SuggestEmojisRequest(**kwargs)).model_dump()

        async def _asuggest_emojis(**kwargs: Any) -> Any:
            logger.debug("EmojiMatchToolkit.get_tools: calling suggest_emojis (async)")
            return (await self.client.asuggest_emojis(SuggestEmojisRequest(**kwargs))).model_dump()

        return [
            StructuredTool.from_function(
                func=_suggest_emojis,
                coroutine=_asuggest_emojis,
                name="suggest_emojis",
                description="Suggests 1-5 emoji matching a text's lexicon, English/French best-supported ($0.001, x402)",
                args_schema=SuggestEmojisRequest,
            ),
        ]
