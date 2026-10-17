"""LangChain `StructuredTool`s for 🩹 extract-correct-service, grouped in one `BaseToolkit` -- one tool per operation, each with both a sync and an async implementation. Requires the `langchain` extra: pip install "xyz17711-extract-correct[langchain]"."""

from __future__ import annotations

import logging
from typing import Any, List, Optional

from langchain_core.tools import BaseTool, BaseToolkit, StructuredTool

from .client import Client
from .models import *  # noqa: F401,F403 -- request models reused as tool args_schema

logger = logging.getLogger(__name__)


class ExtractCorrectToolkit(BaseToolkit):
    """LangChain toolkit for 🩹 extract-correct-service -- one StructuredTool per operation, reusing this package's own generated client and request models directly. Each tool carries both a sync and an async (`coroutine=`) implementation, so `.invoke()` and `.ainvoke()` both work."""

    client: Client
    model_config = {"arbitrary_types_allowed": True}

    def get_tools(self) -> List[BaseTool]:
        logger.debug("ExtractCorrectToolkit.get_tools: building 1 tool(s)")
        def _parse_json(**kwargs: Any) -> Any:
            logger.debug("ExtractCorrectToolkit.get_tools: calling parse_json")
            return self.client.parse_json(ParseJsonRequest(**kwargs)).model_dump()

        async def _aparse_json(**kwargs: Any) -> Any:
            logger.debug("ExtractCorrectToolkit.get_tools: calling parse_json (async)")
            return (await self.client.aparse_json(ParseJsonRequest(**kwargs))).model_dump()

        return [
            StructuredTool.from_function(
                func=_parse_json,
                coroutine=_aparse_json,
                name="parse_json",
                description="JSON repair API: extract valid JSON from messy text or model output and fix it against a JSON Schema ($0.006, x402)",
                args_schema=ParseJsonRequest,
            ),
        ]
