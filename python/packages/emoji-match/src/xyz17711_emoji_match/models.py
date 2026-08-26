"""Pydantic request/response models for emoji-match-service."""

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class SuggestEmojisResponse(BaseModel):
    emojis: List[str]  # 1 to 5 emoji matching the text's lexicon/meaning, most relevant first.
    matched_language: str  # Which language (ISO 639-1 code, e.g. "en"/"fr") the best match was found in -- the input is stemmed and scored against every supported language, and this reports which one actually produced the result, useful to gauge match confidence for an unfamiliar language.

    @classmethod
    def _dummy(cls) -> "SuggestEmojisResponse":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(emojis=[], matched_language="test")


class SuggestEmojisRequest(BaseModel):
    text: str  # The text to analyze. Works best in English or French; best-effort for 16 other languages (see the tool's own description). Truncated to a reasonable length before analysis if very long -- the response reflects the truncated text, not the full input.

    @classmethod
    def _dummy(cls) -> "SuggestEmojisRequest":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(text="test")
