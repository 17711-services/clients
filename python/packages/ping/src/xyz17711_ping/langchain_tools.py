"""LangChain `StructuredTool`s for ping-service, grouped in one `BaseToolkit` -- one tool per operation, each with both a sync and an async implementation. Requires the `langchain` extra: pip install "xyz17711-ping[langchain]"."""

from __future__ import annotations

import logging
from typing import Any, List, Optional

from langchain_core.tools import BaseTool, BaseToolkit, StructuredTool

from .client import Client
from .models import *  # noqa: F401,F403 -- request models reused as tool args_schema

logger = logging.getLogger(__name__)


class PingToolkit(BaseToolkit):
    """LangChain toolkit for ping-service -- one StructuredTool per operation, reusing this package's own generated client and request models directly. Each tool carries both a sync and an async (`coroutine=`) implementation, so `.invoke()` and `.ainvoke()` both work."""

    client: Client
    model_config = {"arbitrary_types_allowed": True}

    def get_tools(self) -> List[BaseTool]:
        logger.debug("PingToolkit.get_tools: building 1 tool(s)")
        def _ping(**kwargs: Any) -> Any:
            logger.debug("PingToolkit.get_tools: calling ping")
            return self.client.ping(PingRequest(**kwargs)).model_dump()

        async def _aping(**kwargs: Any) -> Any:
            logger.debug("PingToolkit.get_tools: calling ping (async)")
            return (await self.client.aping(PingRequest(**kwargs))).model_dump()

        return [
            StructuredTool.from_function(
                func=_ping,
                coroutine=_aping,
                name="ping",
                description="Echoes back the input plus this process's pid ($0.001, x402)",
                args_schema=PingRequest,
            ),
        ]
