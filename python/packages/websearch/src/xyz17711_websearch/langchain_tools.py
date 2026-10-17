"""LangChain `StructuredTool`s for websearch, grouped in one `BaseToolkit` -- one tool per operation, each with both a sync and an async implementation. Requires the `langchain` extra: pip install "xyz17711-websearch[langchain]"."""

from __future__ import annotations

import logging
from typing import Any, List, Optional

from langchain_core.tools import BaseTool, BaseToolkit, StructuredTool

from .client import Client
from .models import *  # noqa: F401,F403 -- request models reused as tool args_schema

logger = logging.getLogger(__name__)


class WebsearchToolkit(BaseToolkit):
    """LangChain toolkit for websearch -- one StructuredTool per operation, reusing this package's own generated client and request models directly. Each tool carries both a sync and an async (`coroutine=`) implementation, so `.invoke()` and `.ainvoke()` both work."""

    client: Client
    model_config = {"arbitrary_types_allowed": True}

    def get_tools(self) -> List[BaseTool]:
        logger.debug("WebsearchToolkit.get_tools: building 3 tool(s)")
        def _get_task_status(**kwargs: Any) -> Any:
            logger.debug("WebsearchToolkit.get_tools: calling get_task_status")
            return self.client.get_task_status(GetTaskStatusRequest(**kwargs)).model_dump()

        async def _aget_task_status(**kwargs: Any) -> Any:
            logger.debug("WebsearchToolkit.get_tools: calling get_task_status (async)")
            return (await self.client.aget_task_status(GetTaskStatusRequest(**kwargs))).model_dump()

        def _search_web(**kwargs: Any) -> Any:
            logger.debug("WebsearchToolkit.get_tools: calling search_web")
            return self.client.search_web(SearchWebRequest(**kwargs)).model_dump()

        async def _asearch_web(**kwargs: Any) -> Any:
            logger.debug("WebsearchToolkit.get_tools: calling search_web (async)")
            return (await self.client.asearch_web(SearchWebRequest(**kwargs))).model_dump()

        def _search_web_async(**kwargs: Any) -> Any:
            logger.debug("WebsearchToolkit.get_tools: calling search_web_async")
            return self.client.search_web_async(SearchWebAsyncRequest(**kwargs)).model_dump()

        async def _asearch_web_async(**kwargs: Any) -> Any:
            logger.debug("WebsearchToolkit.get_tools: calling search_web_async (async)")
            return (await self.client.asearch_web_async(SearchWebAsyncRequest(**kwargs))).model_dump()

        return [
            StructuredTool.from_function(
                func=_get_task_status,
                coroutine=_aget_task_status,
                name="get_task_status",
                description="Polls for the result of a task enqueued by a *_async tool",
                args_schema=GetTaskStatusRequest,
            ),
            StructuredTool.from_function(
                func=_search_web,
                coroutine=_asearch_web,
                name="search_web",
                description="Web search API for agents: search the web and get result titles, URLs and snippets as JSON ($0.005, x402)",
                args_schema=SearchWebRequest,
            ),
            StructuredTool.from_function(
                func=_search_web_async,
                coroutine=_asearch_web_async,
                name="search_web_async",
                description="[Deprecated - use websearch_search_web] Enqueues a websearch_search_web job and returns a task id immediately ($0.005, x402)",
                args_schema=SearchWebAsyncRequest,
            ),
        ]
