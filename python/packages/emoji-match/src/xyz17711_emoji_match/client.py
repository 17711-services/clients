"""Typed HTTP client for emoji-match-service -- one method per operation, each with a sync form and an async (`a`-prefixed) form."""

from __future__ import annotations

import logging

from xyz17711_core import Client as _BaseClient

from .models import *  # noqa: F401,F403 -- re-exported for callers building requests

logger = logging.getLogger(__name__)


class Client(_BaseClient):
    """Typed client for emoji-match-service. Every method has a sync form and an async form (the `a`-prefixed sibling, e.g. `asuggest_emojis` next to `suggest_emojis`) sharing the same underlying connection/wallet -- pick whichever fits your own code."""

    def suggest_emojis(self, request: SuggestEmojisRequest) -> SuggestEmojisResponse:
        """Emoji suggestion API: text in 18 languages in, the 1 to 5 best matching emoji out, deterministic and fast ($0.002, x402)"""
        logger.debug("suggest_emojis: calling %s", "/v1/emoji-match/suggest_emojis")
        return SuggestEmojisResponse.model_validate(self._post("/v1/emoji-match/suggest_emojis", request.model_dump(mode="json", exclude_none=True)))

    async def asuggest_emojis(self, request: SuggestEmojisRequest) -> SuggestEmojisResponse:
        """Emoji suggestion API: text in 18 languages in, the 1 to 5 best matching emoji out, deterministic and fast ($0.002, x402) (async)"""
        logger.debug("asuggest_emojis: calling %s", "/v1/emoji-match/suggest_emojis")
        return SuggestEmojisResponse.model_validate(await self._apost("/v1/emoji-match/suggest_emojis", request.model_dump(mode="json", exclude_none=True)))

