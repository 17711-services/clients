"""Pydantic request/response models for websearch."""

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


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


class SearchResultItem(BaseModel):
    snippet: str
    title: str
    url: str

    @classmethod
    def _dummy(cls) -> "SearchResultItem":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(snippet="test", title="test", url="test")


class SearchWebResponse(BaseModel):
    results: List[SearchResultItem]

    @classmethod
    def _dummy(cls) -> "SearchWebResponse":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(results=[])


class SearchWebRequest(BaseModel):
    query: str  # The search query text, e.g. `"rust async runtime comparison"`.

    @classmethod
    def _dummy(cls) -> "SearchWebRequest":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(query="test")


class AsyncTaskResponse(BaseModel):
    """The fixed response shape of every `*_async` tool -- deliberately NOT generic over the underlying sync tool's own response type, since no work has actually happened yet at this point."""
    task_id: str

    @classmethod
    def _dummy(cls) -> "AsyncTaskResponse":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(task_id="test")


class SearchWebAsyncRequest(BaseModel):
    callback_url: Optional[str] = None  # When set, the worker that processes this task POSTs the eventual result (a `TaskResult` JSON body) here, best-effort -- polling `websearch_get_task_status` always works too, regardless of whether this is set.
    query: str  # The search query text, e.g. `"rust async runtime comparison"`.

    @classmethod
    def _dummy(cls) -> "SearchWebAsyncRequest":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(callback_url=None, query="test")
