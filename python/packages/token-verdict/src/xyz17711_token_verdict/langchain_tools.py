"""LangChain `StructuredTool`s for token-verdict-service, grouped in one `BaseToolkit` -- one tool per operation, each with both a sync and an async implementation. Requires the `langchain` extra: pip install "xyz17711-token-verdict[langchain]"."""

from __future__ import annotations

import logging
from typing import Any, List, Optional

from langchain_core.tools import BaseTool, BaseToolkit, StructuredTool

from .client import Client
from .models import *  # noqa: F401,F403 -- request models reused as tool args_schema

logger = logging.getLogger(__name__)


class TokenVerdictToolkit(BaseToolkit):
    """LangChain toolkit for token-verdict-service -- one StructuredTool per operation, reusing this package's own generated client and request models directly. Each tool carries both a sync and an async (`coroutine=`) implementation, so `.invoke()` and `.ainvoke()` both work."""

    client: Client
    model_config = {"arbitrary_types_allowed": True}

    def get_tools(self) -> List[BaseTool]:
        logger.debug("TokenVerdictToolkit.get_tools: building 1 tool(s)")
        def _get_verdict(**kwargs: Any) -> Any:
            logger.debug("TokenVerdictToolkit.get_tools: calling get_verdict")
            return self.client.get_verdict(GetVerdictRequest(**kwargs)).model_dump()

        async def _aget_verdict(**kwargs: Any) -> Any:
            logger.debug("TokenVerdictToolkit.get_tools: calling get_verdict (async)")
            return (await self.client.aget_verdict(GetVerdictRequest(**kwargs))).model_dump()

        return [
            StructuredTool.from_function(
                func=_get_verdict,
                coroutine=_aget_verdict,
                name="get_verdict",
                description="Token verdict and security check: is this token safe? Honeypot, rug pull and scam detection with taxes, liquidity and admin powers ($0.01, x402)",
                args_schema=GetVerdictRequest,
            ),
        ]
