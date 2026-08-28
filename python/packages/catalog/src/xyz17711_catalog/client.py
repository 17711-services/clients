"""Typed HTTP client for catalog -- one method per operation, each with a sync form and an async (`a`-prefixed) form."""

from __future__ import annotations

import logging

from xyz17711_core import Client as _BaseClient

from .models import *  # noqa: F401,F403 -- re-exported for callers building requests

logger = logging.getLogger(__name__)


class Client(_BaseClient):
    """Typed client for catalog. Every method has a sync form and an async form (the `a`-prefixed sibling, e.g. `acategory` next to `category`) sharing the same underlying connection/wallet -- pick whichever fits your own code."""

    def category(self, q: str, limit: Optional[int] = None, offset: Optional[int] = None) -> CatalogCategoryResponse:
        """Lists every registration in one category, paginated (public GET)"""
        logger.debug("category: calling %s", "/v1/catalog/category")
        return CatalogCategoryResponse.model_validate(self._get("/v1/catalog/category", {"q": q, "limit": limit, "offset": offset}))

    async def acategory(self, q: str, limit: Optional[int] = None, offset: Optional[int] = None) -> CatalogCategoryResponse:
        """Lists every registration in one category, paginated (public GET) (async)"""
        logger.debug("acategory: calling %s", "/v1/catalog/category")
        return CatalogCategoryResponse.model_validate(await self._aget("/v1/catalog/category", {"q": q, "limit": limit, "offset": offset}))

    def find_services_by_capability(self, request: SearchRequest) -> SearchResponse:
        """Ranks registered services/tools by relevance to a free-text query"""
        logger.debug("find_services_by_capability: calling %s", "/v1/catalog/find_services_by_capability")
        return SearchResponse.model_validate(self._post("/v1/catalog/find_services_by_capability", request.model_dump(mode="json", exclude_none=True)))

    async def afind_services_by_capability(self, request: SearchRequest) -> SearchResponse:
        """Ranks registered services/tools by relevance to a free-text query (async)"""
        logger.debug("afind_services_by_capability: calling %s", "/v1/catalog/find_services_by_capability")
        return SearchResponse.model_validate(await self._apost("/v1/catalog/find_services_by_capability", request.model_dump(mode="json", exclude_none=True)))

    def search(self, q: str, category: Optional[str] = None, limit: Optional[int] = None) -> CatalogSearchResponse:
        """Ranks registered services/tools by relevance to a free-text query (public GET)"""
        logger.debug("search: calling %s", "/v1/catalog/search")
        return CatalogSearchResponse.model_validate(self._get("/v1/catalog/search", {"q": q, "category": category, "limit": limit}))

    async def asearch(self, q: str, category: Optional[str] = None, limit: Optional[int] = None) -> CatalogSearchResponse:
        """Ranks registered services/tools by relevance to a free-text query (public GET) (async)"""
        logger.debug("asearch: calling %s", "/v1/catalog/search")
        return CatalogSearchResponse.model_validate(await self._aget("/v1/catalog/search", {"q": q, "category": category, "limit": limit}))

