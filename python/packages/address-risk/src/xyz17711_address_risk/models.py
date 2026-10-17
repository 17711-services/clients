"""Pydantic request/response models for address-risk-service."""

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class Flag(BaseModel):
    code: str  # Stable code, e.g. `sanctioned`, `phishing`, `theft`, `mixer`, `blacklist_doubt`.
    message: str
    severity: str  # `critical`, `high` or `medium`.

    @classmethod
    def _dummy(cls) -> "Flag":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(code="test", message="test", severity="test")


class CheckAddressResponse(BaseModel):
    address: str
    age_seconds: int  # How old this result is, in seconds (0 for a fresh check).
    chain: str
    disclaimer: str
    flags: List[Flag]  # Every flag raised, most severe first. Empty when the verdict is `clear`.
    from_cache: bool  # `true` when served from a stored result.
    kind: str  # `contract` or `wallet`.
    reported_by: Optional[str] = None  # Who reported the address, when the source says (e.g. `SlowMist,BlockSec`).
    retrieved_at: str  # When the data was read (UTC).
    safety_score: int  # 0 to 100, higher is safer; derived from the flags.
    verdict: str  # `clear` (no known flag), `caution`, `risky` or `dangerous`. `clear` means no report was found, not that the address is guaranteed safe.

    @classmethod
    def _dummy(cls) -> "CheckAddressResponse":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(address="test", age_seconds=0, chain="test", disclaimer="test", flags=[], from_cache=False, kind="test", reported_by=None, retrieved_at="test", safety_score=0, verdict="test")


class CheckAddressRequest(BaseModel):
    address: str  # The wallet or contract address to screen (`0x` followed by 40 hex characters).
    chain: Optional[str] = None  # The chain: `base` (default), `ethereum`, `bsc`, `polygon`, `arbitrum`, `optimism` or `avalanche`.
    max_age_seconds: Optional[int] = None  # The oldest result you accept, in seconds. Omit it for the default (up to 10 minutes old); `0` forces a fresh check. The response always says how old it is.

    @classmethod
    def _dummy(cls) -> "CheckAddressRequest":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(address="test", chain=None, max_age_seconds=None)
