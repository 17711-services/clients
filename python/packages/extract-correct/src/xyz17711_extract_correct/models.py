"""Pydantic request/response models for extract-correct-service."""

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class AppliedFix(BaseModel):
    """One deterministic correction actually applied to the extracted value."""
    detail: str  # Human-readable detail of what changed.
    path: str  # JSON Pointer to the field that was corrected (e.g. `/user/age`; `""` = the whole value).
    rule: str  # Which bounded correction rule fired (e.g. `type_coercion`, `additional_property_stripped`, `enum_case_insensitive_match`, `required_default_filled`, `clamped_to_minimum`, `clamped_to_maximum`, `array_truncated_to_max_items`).

    @classmethod
    def _dummy(cls) -> "AppliedFix":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(detail="test", path="test", rule="test")


class RemainingIssue(BaseModel):
    """One schema violation that could NOT be corrected -- never silently dropped or guessed."""
    keyword: str  # The JSON Schema keyword that failed (e.g. `pattern`, `format`, `minItems`, `oneOf`).
    message: str  # The underlying validator's own error message.
    path: str  # JSON Pointer to the field that still fails validation.

    @classmethod
    def _dummy(cls) -> "RemainingIssue":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(keyword="test", message="test", path="test")


class ParseJsonResponse(BaseModel):
    applied_fixes: List[AppliedFix]  # Every correction actually applied, in the order applied.
    data: Any  # The extracted (and, if a schema was supplied, corrected) JSON value.
    extraction_method: str  # How `data` was obtained: `"direct"` (already valid JSON), `"repaired"` (malformed JSON fixed in place), or `"extracted_and_repaired"` (isolated from surrounding text, then fixed).
    remaining_issues: List[RemainingIssue]  # Every schema violation that remains after correction -- non-empty only when `schema` was supplied and at least one issue couldn't be fixed by a bounded v1 rule.
    valid: Optional[bool] = None  # Whether `data` satisfies `schema` after correction. `None` when no `schema` was supplied -- never conflated with "assumed valid".

    @classmethod
    def _dummy(cls) -> "ParseJsonResponse":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(applied_fixes=[], data=None, extraction_method="test", remaining_issues=[], valid=None)


class ParseJsonRequest(BaseModel):
    schema: Optional[Any] = None  # Optional JSON Schema to validate the extracted value against and auto-correct where a bounded, deterministic fix rule applies. Omitted = extraction only, no validation.
    text: str  # Free-form or messy text to extract structured JSON from -- already-valid JSON, JSON wrapped in prose or a markdown code fence, or malformed JSON (trailing commas, single-quoted strings, unquoted keys, a truncated array/object).

    @classmethod
    def _dummy(cls) -> "ParseJsonRequest":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(schema=None, text="test")
