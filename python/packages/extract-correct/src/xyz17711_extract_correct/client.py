"""Typed HTTP client for 🩹 extract-correct-service -- one method per operation, each with a sync form and an async (`a`-prefixed) form."""

from __future__ import annotations

import logging

from xyz17711_core import Client as _BaseClient

from .models import *  # noqa: F401,F403 -- re-exported for callers building requests

logger = logging.getLogger(__name__)


class Client(_BaseClient):
    """Typed client for 🩹 extract-correct-service. Every method has a sync form and an async form (the `a`-prefixed sibling, e.g. `aparse_json` next to `parse_json`) sharing the same underlying connection/wallet -- pick whichever fits your own code."""

    def parse_json(self, request: ParseJsonRequest) -> ParseJsonResponse:
        """JSON repair API: extract valid JSON from messy text or model output and fix it against a JSON Schema ($0.006, x402)"""
        logger.debug("parse_json: calling %s", "/v1/extract-correct/parse_json")
        return ParseJsonResponse.model_validate(self._post("/v1/extract-correct/parse_json", request.model_dump(mode="json", exclude_none=True)))

    async def aparse_json(self, request: ParseJsonRequest) -> ParseJsonResponse:
        """JSON repair API: extract valid JSON from messy text or model output and fix it against a JSON Schema ($0.006, x402) (async)"""
        logger.debug("aparse_json: calling %s", "/v1/extract-correct/parse_json")
        return ParseJsonResponse.model_validate(await self._apost("/v1/extract-correct/parse_json", request.model_dump(mode="json", exclude_none=True)))

