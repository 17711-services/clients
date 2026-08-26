"""Pydantic request/response models for proxy-pool."""

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class ProxyView(BaseModel):
    """A `SourceProxy` joined with its `CheckedProxy` result, if it has been checked at least once -- what every read tool actually filters/returns."""
    anonymity: str
    checked_alive: Optional[bool] = None  # `None` if this service has never checked this proxy yet.
    checked_at: Optional[int] = None
    checked_consecutive_successes: int  # See `CheckedProxy::consecutive_successes`'s own doc comment. `0` if never checked.
    checked_ema_latency_ms: Optional[float] = None  # See `CheckedProxy::ema_latency_ms`'s own doc comment.
    checked_latency_ms: Optional[int] = None
    checked_protocol: Optional[str] = None
    city: str
    country: str
    id: str
    ip: str
    port: int
    protocols: List[str]

    @classmethod
    def _dummy(cls) -> "ProxyView":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(anonymity="test", checked_alive=None, checked_at=None, checked_consecutive_successes=0, checked_ema_latency_ms=None, checked_latency_ms=None, checked_protocol=None, city="test", country="test", id="test", ip="test", port=0, protocols=[])


class GetBestProxyResponse(BaseModel):
    proxy: ProxyView

    @classmethod
    def _dummy(cls) -> "GetBestProxyResponse":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(proxy=ProxyView._dummy())
