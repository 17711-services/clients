"""Typed HTTP client for emoji-match-service -- one method per operation, each with a sync form and an async (`a`-prefixed) form."""

from __future__ import annotations

import logging
from typing import Optional

from xyz17711_core import Client as _BaseClient

from .models import *  # noqa: F401,F403 -- re-exported for callers building requests

logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = "https://api.17711.xyz/registry/emoji-match-service"
"""Production base URL of this service; pass another `base_url` to self-host or test."""


class Client(_BaseClient):
    """Typed client for emoji-match-service. Every method has a sync form and an async form (the `a`-prefixed sibling, e.g. `asuggest_emojis` next to `suggest_emojis`) sharing the same underlying connection/wallet -- pick whichever fits your own code."""

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        *,
        timeout: float = 30.0,
        x402_private_key: Optional[str] = None,
        x402_expected_network: Optional[str] = None,
        x402_max_payment_usdc: Optional[float] = None,
        x402_max_total_spend_usdc: Optional[float] = None,
    ):
        super().__init__(
            base_url,
            timeout=timeout,
            x402_private_key=x402_private_key,
            x402_expected_network=x402_expected_network,
            x402_max_payment_usdc=x402_max_payment_usdc,
            x402_max_total_spend_usdc=x402_max_total_spend_usdc,
        )

    def suggest_emojis(self, request: SuggestEmojisRequest) -> SuggestEmojisResponse:
        """Emoji suggestion API: text in 18 languages in, the 1 to 5 best matching emoji out, deterministic and fast ($0.002, x402)"""
        logger.debug("suggest_emojis: calling %s", "/v1/emoji-match/suggest_emojis")
        return SuggestEmojisResponse.model_validate(self._post("/v1/emoji-match/suggest_emojis", request.model_dump(mode="json", exclude_none=True)))

    async def asuggest_emojis(self, request: SuggestEmojisRequest) -> SuggestEmojisResponse:
        """Emoji suggestion API: text in 18 languages in, the 1 to 5 best matching emoji out, deterministic and fast ($0.002, x402) (async)"""
        logger.debug("asuggest_emojis: calling %s", "/v1/emoji-match/suggest_emojis")
        return SuggestEmojisResponse.model_validate(await self._apost("/v1/emoji-match/suggest_emojis", request.model_dump(mode="json", exclude_none=True)))

