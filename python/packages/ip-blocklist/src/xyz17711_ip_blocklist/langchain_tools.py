"""LangChain `StructuredTool`s for ip-blocklist, grouped in one `BaseToolkit` -- one tool per operation, each with both a sync and an async implementation. Requires the `langchain` extra: pip install "xyz17711-ip-blocklist[langchain]"."""

from __future__ import annotations

import logging
from typing import Any, List, Optional

from langchain_core.tools import BaseTool, BaseToolkit, StructuredTool

from .client import Client
from .models import *  # noqa: F401,F403 -- request models reused as tool args_schema

logger = logging.getLogger(__name__)


class IpBlocklistToolkit(BaseToolkit):
    """LangChain toolkit for ip-blocklist -- one StructuredTool per operation, reusing this package's own generated client and request models directly. Each tool carries both a sync and an async (`coroutine=`) implementation, so `.invoke()` and `.ainvoke()` both work."""

    client: Client
    model_config = {"arbitrary_types_allowed": True}

    def get_tools(self) -> List[BaseTool]:
        logger.debug("IpBlocklistToolkit.get_tools: building 1 tool(s)")
        def _check_ip(ip: str) -> Any:
            logger.debug("IpBlocklistToolkit.get_tools: calling check_ip")
            return self.client.check_ip(ip=ip).model_dump()

        async def _acheck_ip(ip: str) -> Any:
            logger.debug("IpBlocklistToolkit.get_tools: calling check_ip (async)")
            return (await self.client.acheck_ip(ip=ip)).model_dump()

        return [
            StructuredTool.from_function(
                func=_check_ip,
                coroutine=_acheck_ip,
                name="check_ip",
                description="IP reputation check: is this IPv4 address on a public threat blocklist (Tor exit nodes, botnets, spam networks) ($0.010, x402)",
            ),
        ]
