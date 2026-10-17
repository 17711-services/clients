"""Typed HTTP client for websearch -- one method per operation, each with a sync form and an async (`a`-prefixed) form."""

from __future__ import annotations

import logging

from xyz17711_core import Client as _BaseClient

from .models import *  # noqa: F401,F403 -- re-exported for callers building requests

logger = logging.getLogger(__name__)


class Client(_BaseClient):
    """Typed client for websearch. Every method has a sync form and an async form (the `a`-prefixed sibling, e.g. `aget_task_status` next to `get_task_status`) sharing the same underlying connection/wallet -- pick whichever fits your own code."""

    def get_task_status(self, request: GetTaskStatusRequest) -> GetTaskStatusResponse:
        """Polls for the result of a task enqueued by a *_async tool"""
        logger.debug("get_task_status: calling %s", "/v1/websearch/get_task_status")
        return GetTaskStatusResponse.model_validate(self._post("/v1/websearch/get_task_status", request.model_dump(mode="json", exclude_none=True)))

    async def aget_task_status(self, request: GetTaskStatusRequest) -> GetTaskStatusResponse:
        """Polls for the result of a task enqueued by a *_async tool (async)"""
        logger.debug("aget_task_status: calling %s", "/v1/websearch/get_task_status")
        return GetTaskStatusResponse.model_validate(await self._apost("/v1/websearch/get_task_status", request.model_dump(mode="json", exclude_none=True)))

    def search_web(self, request: SearchWebRequest) -> SearchWebResponse:
        """Web search API for agents: search the web and get result titles, URLs and snippets as JSON ($0.005, x402)"""
        logger.debug("search_web: calling %s", "/v1/websearch/search_web")
        return SearchWebResponse.model_validate(self._post("/v1/websearch/search_web", request.model_dump(mode="json", exclude_none=True)))

    async def asearch_web(self, request: SearchWebRequest) -> SearchWebResponse:
        """Web search API for agents: search the web and get result titles, URLs and snippets as JSON ($0.005, x402) (async)"""
        logger.debug("asearch_web: calling %s", "/v1/websearch/search_web")
        return SearchWebResponse.model_validate(await self._apost("/v1/websearch/search_web", request.model_dump(mode="json", exclude_none=True)))

    def search_web_async(self, request: SearchWebAsyncRequest) -> AsyncTaskResponse:
        """[Deprecated - use websearch_search_web] Enqueues a websearch_search_web job and returns a task id immediately ($0.005, x402)"""
        logger.debug("search_web_async: calling %s", "/v1/websearch/search_web_async")
        return AsyncTaskResponse.model_validate(self._post("/v1/websearch/search_web_async", request.model_dump(mode="json", exclude_none=True)))

    async def asearch_web_async(self, request: SearchWebAsyncRequest) -> AsyncTaskResponse:
        """[Deprecated - use websearch_search_web] Enqueues a websearch_search_web job and returns a task id immediately ($0.005, x402) (async)"""
        logger.debug("asearch_web_async: calling %s", "/v1/websearch/search_web_async")
        return AsyncTaskResponse.model_validate(await self._apost("/v1/websearch/search_web_async", request.model_dump(mode="json", exclude_none=True)))

