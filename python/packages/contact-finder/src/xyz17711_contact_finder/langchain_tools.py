"""LangChain `StructuredTool`s for contact-finder-service, grouped in one `BaseToolkit` -- one tool per operation, each with both a sync and an async implementation. Requires the `langchain` extra: pip install "xyz17711-contact-finder[langchain]"."""

from __future__ import annotations

import logging
from typing import Any, List, Optional

from langchain_core.tools import BaseTool, BaseToolkit, StructuredTool

from .client import Client
from .models import *  # noqa: F401,F403 -- request models reused as tool args_schema

logger = logging.getLogger(__name__)


class ContactFinderToolkit(BaseToolkit):
    """LangChain toolkit for contact-finder-service -- one StructuredTool per operation, reusing this package's own generated client and request models directly. Each tool carries both a sync and an async (`coroutine=`) implementation, so `.invoke()` and `.ainvoke()` both work."""

    client: Client
    model_config = {"arbitrary_types_allowed": True}

    def get_tools(self) -> List[BaseTool]:
        logger.debug("ContactFinderToolkit.get_tools: building 1 tool(s)")
        def _get_contacts(**kwargs: Any) -> Any:
            logger.debug("ContactFinderToolkit.get_tools: calling get_contacts")
            return self.client.get_contacts(GetContactsRequest(**kwargs)).model_dump()

        async def _aget_contacts(**kwargs: Any) -> Any:
            logger.debug("ContactFinderToolkit.get_tools: calling get_contacts (async)")
            return (await self.client.aget_contacts(GetContactsRequest(**kwargs))).model_dump()

        return [
            StructuredTool.from_function(
                func=_get_contacts,
                coroutine=_aget_contacts,
                name="get_contacts",
                description="Contact finder: public business emails, phone numbers, contact forms and support pages of a domain, with role and source ($0.009, x402)",
                args_schema=GetContactsRequest,
            ),
        ]
