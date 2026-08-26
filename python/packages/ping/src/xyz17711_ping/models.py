"""Pydantic request/response models for ping-service."""

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class PingResult(BaseModel):
    echo: str  # Echoes the request's own `echo` field back verbatim.
    pid: int  # This process's OS pid -- proves which process instance actually answered (useful behind a load balancer fronting several instances of the same service).
    pong: bool  # Always `true` -- a client can use this as a trivial liveness/reachability check.

    @classmethod
    def _dummy(cls) -> "PingResult":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(echo="test", pid=0, pong=False)


class PingRequest(BaseModel):
    delay_ms: Optional[int] = None  # Testkit-only knob (not real business logic): lets a caller simulate a slow tool call, to check whether the server dispatches concurrent calls as independent tasks rather than serializing them.
    echo: str  # Arbitrary text echoed back verbatim in the response's own `echo` field.

    @classmethod
    def _dummy(cls) -> "PingRequest":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(delay_ms=None, echo="test")
