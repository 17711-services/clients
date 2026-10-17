"""LangChain `StructuredTool`s for 🛑 address-risk-service, grouped in one `BaseToolkit` -- one tool per operation, each with both a sync and an async implementation. Requires the `langchain` extra: pip install "xyz17711-address-risk[langchain]"."""

from __future__ import annotations

import logging
from typing import Any, List, Optional

from langchain_core.tools import BaseTool, BaseToolkit, StructuredTool

from .client import Client
from .models import *  # noqa: F401,F403 -- request models reused as tool args_schema

logger = logging.getLogger(__name__)


class AddressRiskToolkit(BaseToolkit):
    """LangChain toolkit for 🛑 address-risk-service -- one StructuredTool per operation, reusing this package's own generated client and request models directly. Each tool carries both a sync and an async (`coroutine=`) implementation, so `.invoke()` and `.ainvoke()` both work."""

    client: Client
    model_config = {"arbitrary_types_allowed": True}

    def get_tools(self) -> List[BaseTool]:
        logger.debug("AddressRiskToolkit.get_tools: building 1 tool(s)")
        def _check_address(**kwargs: Any) -> Any:
            logger.debug("AddressRiskToolkit.get_tools: calling check_address")
            return self.client.check_address(CheckAddressRequest(**kwargs)).model_dump()

        async def _acheck_address(**kwargs: Any) -> Any:
            logger.debug("AddressRiskToolkit.get_tools: calling check_address (async)")
            return (await self.client.acheck_address(CheckAddressRequest(**kwargs))).model_dump()

        return [
            StructuredTool.from_function(
                func=_check_address,
                coroutine=_acheck_address,
                name="check_address",
                description="Wallet address risk check: sanctioned address and phishing check for a crypto wallet or contract before you send funds, with theft, scam, mixer and blacklist flags ($0.005, x402)",
                args_schema=CheckAddressRequest,
            ),
        ]
