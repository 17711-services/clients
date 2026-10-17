"""Typed HTTP client for 📇 contact-finder-service -- one method per operation, each with a sync form and an async (`a`-prefixed) form."""

from __future__ import annotations

import logging

from xyz17711_core import Client as _BaseClient

from .models import *  # noqa: F401,F403 -- re-exported for callers building requests

logger = logging.getLogger(__name__)


class Client(_BaseClient):
    """Typed client for 📇 contact-finder-service. Every method has a sync form and an async form (the `a`-prefixed sibling, e.g. `aget_contacts` next to `get_contacts`) sharing the same underlying connection/wallet -- pick whichever fits your own code."""

    def get_contacts(self, request: GetContactsRequest) -> GetContactsResponse:
        """Contact finder: public business emails, phone numbers, contact forms and support pages of a domain, with role and source ($0.009, x402)"""
        logger.debug("get_contacts: calling %s", "/v1/contact-finder/get_contacts")
        return GetContactsResponse.model_validate(self._post("/v1/contact-finder/get_contacts", request.model_dump(mode="json", exclude_none=True)))

    async def aget_contacts(self, request: GetContactsRequest) -> GetContactsResponse:
        """Contact finder: public business emails, phone numbers, contact forms and support pages of a domain, with role and source ($0.009, x402) (async)"""
        logger.debug("aget_contacts: calling %s", "/v1/contact-finder/get_contacts")
        return GetContactsResponse.model_validate(await self._apost("/v1/contact-finder/get_contacts", request.model_dump(mode="json", exclude_none=True)))

