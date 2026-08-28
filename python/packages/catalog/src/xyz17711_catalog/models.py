"""Pydantic request/response models for catalog."""

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class CatalogCategoryEntry(BaseModel):
    category: str
    description: str
    host: str
    name: str
    port: int
    registered_at: int

    @classmethod
    def _dummy(cls) -> "CatalogCategoryEntry":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(category="test", description="test", host="test", name="test", port=0, registered_at=0)


class CatalogCategoryResponse(BaseModel):
    entries: List[CatalogCategoryEntry]  # This page's entries, in no particular order (no ranking -- this is a listing, not a search).
    limit: int
    offset: int
    total_count: int  # Total number of registrations matching `q`, BEFORE `limit`/`offset` are applied -- lets a caller know whether more pages remain.

    @classmethod
    def _dummy(cls) -> "CatalogCategoryResponse":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(entries=[], limit=0, offset=0, total_count=0)


class SearchResult(BaseModel):
    description: str
    host: str
    method: str
    port: int
    price_usdc: str  # Decimal USDC string (e.g. `"0.01"`), or `""` if this tool is free -- structural pricing, not just prose in `description`.
    route: str
    score: float  # Similarity score (semantic embedding cosine similarity when available, else keyword overlap in `[0, 1]`) -- higher is a better match. Not comparable across two different searches (the scoring method may differ per-call depending on embedding availability).
    service_name: str
    tool_name: str

    @classmethod
    def _dummy(cls) -> "SearchResult":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(description="test", host="test", method="test", port=0, price_usdc="test", route="test", score=0.0, service_name="test", tool_name="test")


class SearchResponse(BaseModel):
    results: List[SearchResult]  # Ranked best-match-first, truncated to the request's own `top_k`.

    @classmethod
    def _dummy(cls) -> "SearchResponse":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(results=[])


class SearchRequest(BaseModel):
    query: str  # Free-text description of the task to find a service for.
    top_k: Optional[int] = None  # Max number of results to return.

    @classmethod
    def _dummy(cls) -> "SearchRequest":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(query="test", top_k=None)


class CatalogSearchResult(BaseModel):
    category: str
    description: str
    host: str
    method: str
    port: int
    price_usdc: str  # Decimal USDC string (e.g. `"0.01"`), or `""` if this tool is free -- structural pricing, not just prose in `description`.
    route: str
    score: float  # Similarity score (semantic embedding cosine similarity when available, else keyword overlap in `[0, 1]`) -- higher is a better match. Not comparable across two different searches (the scoring method may differ per-call depending on embedding availability).
    service_name: str
    tool_name: str

    @classmethod
    def _dummy(cls) -> "CatalogSearchResult":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(category="test", description="test", host="test", method="test", port=0, price_usdc="test", route="test", score=0.0, service_name="test", tool_name="test")


class CatalogSearchResponse(BaseModel):
    results: List[CatalogSearchResult]  # Ranked best-match-first, truncated to the request's own `limit`.

    @classmethod
    def _dummy(cls) -> "CatalogSearchResponse":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(results=[])
