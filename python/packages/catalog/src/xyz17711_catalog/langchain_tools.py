"""LangChain `StructuredTool`s for catalog, grouped in one `BaseToolkit` -- one tool per operation, each with both a sync and an async implementation. Requires the `langchain` extra: pip install "xyz17711-catalog[langchain]"."""

from __future__ import annotations

import logging
from typing import Any, List, Optional

from langchain_core.tools import BaseTool, BaseToolkit, StructuredTool

from .client import Client
from .models import *  # noqa: F401,F403 -- request models reused as tool args_schema

logger = logging.getLogger(__name__)


class CatalogToolkit(BaseToolkit):
    """LangChain toolkit for catalog -- one StructuredTool per operation, reusing this package's own generated client and request models directly. Each tool carries both a sync and an async (`coroutine=`) implementation, so `.invoke()` and `.ainvoke()` both work."""

    client: Client
    model_config = {"arbitrary_types_allowed": True}

    def get_tools(self) -> List[BaseTool]:
        logger.debug("CatalogToolkit.get_tools: building 3 tool(s)")
        def _category(q: str, limit: Optional[int] = None, offset: Optional[int] = None) -> Any:
            logger.debug("CatalogToolkit.get_tools: calling category")
            return self.client.category(q=q, limit=limit, offset=offset).model_dump()

        async def _acategory(q: str, limit: Optional[int] = None, offset: Optional[int] = None) -> Any:
            logger.debug("CatalogToolkit.get_tools: calling category (async)")
            return (await self.client.acategory(q=q, limit=limit, offset=offset)).model_dump()

        def _find_services_by_capability(**kwargs: Any) -> Any:
            logger.debug("CatalogToolkit.get_tools: calling find_services_by_capability")
            return self.client.find_services_by_capability(SearchRequest(**kwargs)).model_dump()

        async def _afind_services_by_capability(**kwargs: Any) -> Any:
            logger.debug("CatalogToolkit.get_tools: calling find_services_by_capability (async)")
            return (await self.client.afind_services_by_capability(SearchRequest(**kwargs))).model_dump()

        def _search(q: str, category: Optional[str] = None, limit: Optional[int] = None) -> Any:
            logger.debug("CatalogToolkit.get_tools: calling search")
            return self.client.search(q=q, category=category, limit=limit).model_dump()

        async def _asearch(q: str, category: Optional[str] = None, limit: Optional[int] = None) -> Any:
            logger.debug("CatalogToolkit.get_tools: calling search (async)")
            return (await self.client.asearch(q=q, category=category, limit=limit)).model_dump()

        return [
            StructuredTool.from_function(
                func=_category,
                coroutine=_acategory,
                name="category",
                description="Lists every registration in one category, paginated (public GET)",
            ),
            StructuredTool.from_function(
                func=_find_services_by_capability,
                coroutine=_afind_services_by_capability,
                name="find_services_by_capability",
                description="Ranks registered services/tools by relevance to a free-text query",
                args_schema=SearchRequest,
            ),
            StructuredTool.from_function(
                func=_search,
                coroutine=_asearch,
                name="search",
                description="Ranks registered services/tools by relevance to a free-text query (public GET)",
            ),
        ]
