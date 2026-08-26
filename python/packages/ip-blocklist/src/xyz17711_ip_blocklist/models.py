"""Pydantic request/response models for ip-blocklist."""

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class BlocklistMatch(BaseModel):
    cidr: str  # The specific CIDR entry from that source that contains the queried IP.
    source: str  # Which source matched, e.g. `"firehol-level1"`.

    @classmethod
    def _dummy(cls) -> "BlocklistMatch":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(cidr="test", source="test")


class CheckIpResponse(BaseModel):
    banned: bool  # `true` if `matches` is non-empty -- a convenience flag, equivalent to `!matches.is_empty()`.
    ip: str
    matches: List[BlocklistMatch]  # Every source that contains this IP, not just the first one found -- an IP flagged by several sources is a stronger signal than one flagged by a single list.

    @classmethod
    def _dummy(cls) -> "CheckIpResponse":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(banned=False, ip="test", matches=[])
