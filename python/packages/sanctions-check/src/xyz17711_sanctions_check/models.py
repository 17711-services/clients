"""Pydantic request/response models for 🚫 sanctions-check-service."""

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class ListStatus(BaseModel):
    entries: int
    fetched_at: str  # When this service last downloaded the list (UTC).
    list: str
    published: Optional[str] = None  # Publication date announced by the list itself, when it states one.

    @classmethod
    def _dummy(cls) -> "ListStatus":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(entries=0, fetched_at="test", list="test", published=None)


class SanctionMatch(BaseModel):
    aliases: List[str]  # Other names the entry is listed under (at most 5).
    birth_year_consistent: Optional[bool] = None  # `true`/`false` when a `birth_year` was given and the entry publishes birth years.
    birth_years: List[int]  # Published years of birth.
    countries: List[str]  # Nationalities or countries, when published.
    entry_id: str  # The entry's identifier in that list.
    kind: str  # `person`, `entity`, `vessel` or `aircraft`.
    list: str  # `OFAC SDN`, `EU consolidated` or `UN Security Council`.
    listed_name: str  # The listed primary name.
    listed_on: Optional[str] = None  # Date of listing, when published.
    match_type: str  # `exact`, `close` or `possible`.
    matched_alias: Optional[str] = None  # The name or alias that matched, when it is not the primary name.
    programs: List[str]  # Sanctions programmes or regimes.
    remarks: Optional[str] = None  # Published remarks (truncated).
    score: float  # 0 to 1: 1 means the same words (any order); lower means a partial or approximate match.

    @classmethod
    def _dummy(cls) -> "SanctionMatch":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(aliases=[], birth_year_consistent=None, birth_years=[], countries=[], entry_id="test", kind="test", list="test", listed_name="test", listed_on=None, match_type="test", matched_alias=None, programs=[], remarks=None, score=0.0)


class ScreenNameResponse(BaseModel):
    disclaimer: str
    lists_missing: List[str]  # Lists that could not be loaded: the screening did not cover them.
    lists_screened: List[ListStatus]  # The lists that were screened, with their size and freshness.
    matches: List[SanctionMatch]  # The best matches, highest score first (at most 10).
    name: str  # The name as screened.
    screened_at: str  # When the screening ran (UTC).
    verdict: str  # `match` (an exact or close match), `possible_match` (a partial match to review) or `no_match`.

    @classmethod
    def _dummy(cls) -> "ScreenNameResponse":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(disclaimer="test", lists_missing=[], lists_screened=[], matches=[], name="test", screened_at="test", verdict="test")


class ScreenNameRequest(BaseModel):
    birth_year: Optional[int] = None  # A person's year of birth. Listed people whose published birth years do not include it are ranked lower and marked `birth_year_consistent: false`.
    name: str  # The name to screen: a person (`Vladimir Putin`, `Putin, Vladimir`) or a company, vessel or organisation. Word order, accents, capitalisation and small spelling variants do not matter.
    type: Optional[str] = None  # Restrict the screening to `person`, `entity`, `vessel` or `aircraft`. Omit it to screen everything.

    @classmethod
    def _dummy(cls) -> "ScreenNameRequest":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(birth_year=None, name="test", type=None)
