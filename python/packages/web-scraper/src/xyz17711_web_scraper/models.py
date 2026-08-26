"""Pydantic request/response models for web-scraper."""

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class ExtractMarkdownResponse(BaseModel):
    content_type: Optional[str] = None
    final_url: str  # The URL actually reached, after any redirects the target sent.
    markdown: str  # Boilerplate-stripped main article content, as Markdown -- navigation, ads, and sidebars removed, not the raw page HTML.
    status: int  # The REAL HTTP status the underlying fetch received.
    title: Optional[str] = None  # Article title, if Readability found one.
    truncated: bool  # `true` if the underlying fetch's HTML was truncated by web-scraper's own fixed byte ceiling (see `web_scraper_scrape_url`'s own `truncated` field) -- `markdown` may then also be incomplete.
    url: str  # The URL as requested, verbatim.

    @classmethod
    def _dummy(cls) -> "ExtractMarkdownResponse":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(content_type=None, final_url="test", markdown="test", status=0, title=None, truncated=False, url="test")


class ExtractMarkdownRequest(BaseModel):
    url: str  # The target URL to fetch, e.g. `"https://example.com/article"`. Must be `http://` or `https://` -- same validation as `web_scraper_scrape_url`, since this tool fetches through the exact same internal scraper.

    @classmethod
    def _dummy(cls) -> "ExtractMarkdownRequest":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(url="test")


class TaskStatusKind(BaseModel):
    """`\"pending\"` (enqueued, no result yet), `\"finished\"` (a worker wrote a result -- see `ok`/ `result`), or `\"unknown\"` (this id was never valid, or both it and its result have expired -- see [`nimpoleon_tasks::TaskState`]'s own doc comment for why this is 3 states, not 2)."""
    pass

    @classmethod
    def _dummy(cls) -> "TaskStatusKind":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls()


class GetTaskStatusResponse(BaseModel):
    ok: Optional[bool] = None
    result: Optional[Any] = None
    status: TaskStatusKind

    @classmethod
    def _dummy(cls) -> "GetTaskStatusResponse":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(ok=None, result=None, status=TaskStatusKind._dummy())


class GetTaskStatusRequest(BaseModel):
    task_id: str  # The `task_id` a `*_async` tool returned.

    @classmethod
    def _dummy(cls) -> "GetTaskStatusRequest":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(task_id="test")


class ScrapeUrlResponse(BaseModel):
    content_type: Optional[str] = None
    final_url: str  # The URL actually reached, after any redirects the target sent.
    html: str  # Raw response body, decoded as UTF-8 (lossy -- see this tool's own description for why), truncated to this service's own fixed byte ceiling if needed.
    status: int  # The REAL HTTP status the target returned -- never masked, never itself a reason to retry.
    truncated: bool  # `true` if `html` was cut short by this service's own fixed byte ceiling.
    url: str  # The URL as requested, verbatim.

    @classmethod
    def _dummy(cls) -> "ScrapeUrlResponse":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(content_type=None, final_url="test", html="test", status=0, truncated=False, url="test")


class ScrapeUrlRequest(BaseModel):
    url: str  # The target URL to fetch, e.g. `"https://example.com/page"`. Must be `http://` or `https://` -- any other scheme is rejected before any fetch is attempted.

    @classmethod
    def _dummy(cls) -> "ScrapeUrlRequest":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(url="test")


class AsyncTaskResponse(BaseModel):
    """The fixed response shape of every `*_async` tool -- deliberately NOT generic over the underlying sync tool's own response type, since no work has actually happened yet at this point."""
    task_id: str

    @classmethod
    def _dummy(cls) -> "AsyncTaskResponse":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(task_id="test")


class ScrapeUrlAsyncRequest(BaseModel):
    callback_url: Optional[str] = None  # When set, the worker that processes this task POSTs the eventual result (a `TaskResult` JSON body) here, best-effort -- polling `web_scraper_get_task_status` always works too, regardless of whether this is set.
    url: str  # The target URL to fetch, e.g. `"https://example.com/page"`. Must be `http://` or `https://` -- any other scheme is rejected before any fetch is attempted.

    @classmethod
    def _dummy(cls) -> "ScrapeUrlAsyncRequest":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(callback_url=None, url="test")
