"""Pydantic request/response models for url-extract-service."""

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class DomainInfo(BaseModel):
    domain_age_years: Optional[float] = None  # Years since registration, one decimal.
    email_provider: Optional[str] = None  # Mail platform deduced from the MX records (`google-workspace`, `microsoft-365`, ...).
    expires_at: Optional[str] = None  # Expiration date, `YYYY-MM-DD`.
    mail_services: List[str]  # Sending services declared in the SPF record (`sendgrid`, `mailchimp`, ...).
    nameservers: List[str]
    registered_at: Optional[str] = None  # Registration date, `YYYY-MM-DD`.
    registrable_domain: str  # The registrable domain the lookups were made for.
    registrant_org: Optional[str] = None  # The registrant, only when it is an organization published in RDAP.
    registrar: Optional[str] = None
    statuses: List[str]  # RDAP status flags (e.g. `client transfer prohibited`), at most 4.

    @classmethod
    def _dummy(cls) -> "DomainInfo":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(domain_age_years=None, email_provider=None, expires_at=None, mail_services=[], nameservers=[], registered_at=None, registrable_domain="test", registrant_org=None, registrar=None, statuses=[])


class GetCompanyProfileResponse(BaseModel):
    applied_fixes: List[Any]  # Every automatic correction applied to the model's answer.
    domain: str  # The host that was profiled, lowercased, without scheme or path.
    domain_info: DomainInfo  # Public registration and DNS facts about the domain: registrar, registration and expiry dates, age, name servers, public registrant organization, mail platform and sending services. Fields that could not be looked up are absent or empty.
    output_language: str  # Language of the profile's free-text values.
    pages_read: List[str]  # The pages that were actually read to build the profile.
    passes: int  # Number of model passes used (2 only when the first answer was incomplete).
    profile: Any  # The profile: `name`, `description`, `offering`, `target_customers`, `pricing_summary`, `headquarters`, `founded`, `contact` (`emails`, `phones`) and `social` (`linkedin`, `twitter`, `github`, `facebook`, `instagram`, `youtube`). A value the pages do not state is `null`.
    remaining_issues: List[Any]  # Every schema violation that could not be corrected.
    resolved_from_name: bool  # `true` when the website was found from `company_name`.
    source_language: str  # Language of the website (ISO 639-1 code).
    unverified_removed: List[str]  # E-mail addresses and social links the model produced that do NOT appear in the pages read; they were removed from `profile` so nothing in it is invented.
    valid: Optional[bool] = None  # Whether the profile satisfies the profile schema after automatic correction.

    @classmethod
    def _dummy(cls) -> "GetCompanyProfileResponse":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(applied_fixes=[], domain="test", domain_info=DomainInfo._dummy(), output_language="test", pages_read=[], passes=0, profile=None, remaining_issues=[], resolved_from_name=False, source_language="test", unverified_removed=[], valid=None)


class GetCompanyProfileRequest(BaseModel):
    company_name: Optional[str] = None  # The company's name, when you do not know its website (e.g. `Mistral AI`): the official site is looked up first. `domain` wins when both are given.
    domain: Optional[str] = None  # The company's website: a domain such as `stripe.com` or a full URL (`https://stripe.com/`). Give this or `company_name`.
    language: Optional[str] = None  # Language of the free-text values of the answer (`en` by default; `fr`, `de`, `es`, `pt-BR`...). The pages may be in any language; the JSON keys are always English.

    @classmethod
    def _dummy(cls) -> "GetCompanyProfileRequest":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(company_name=None, domain=None, language=None)


class GetStructuredDataResponse(BaseModel):
    age_seconds: int  # How old this answer is, in seconds (0 for a fresh read).
    applied_fixes: List[Any]  # Every automatic correction applied to the model's answer, in order.
    data: Any  # The structured answer (an object or an array), corrected against `schema` when one was given.
    final_url: str  # The URL actually read, after redirects.
    from_cache: bool  # `true` when this answer was served from a stored result rather than computed now.
    page_from_cache: bool  # `true` when the page text came from a stored copy (fresh enough for `max_age_seconds`).
    page_truncated: bool  # `true` when the page was longer than the amount of text the answer is based on.
    remaining_issues: List[Any]  # Every schema violation that could not be corrected.
    retrieved_at: str  # When the page was read to build this answer (UTC).
    stale_page: bool  # `true` when the page could not be refreshed and an older stored copy was used.
    title: Optional[str] = None  # The page title, when one could be extracted.
    url: str  # The URL that was requested.
    valid: Optional[bool] = None  # Whether `data` satisfies `schema` after correction; absent when no schema was given.

    @classmethod
    def _dummy(cls) -> "GetStructuredDataResponse":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(age_seconds=0, applied_fixes=[], data=None, final_url="test", from_cache=False, page_from_cache=False, page_truncated=False, remaining_issues=[], retrieved_at="test", stale_page=False, title=None, url="test", valid=None)


class GetStructuredDataRequest(BaseModel):
    max_age_seconds: Optional[int] = None  # The oldest answer you accept, in seconds. Omit it for the default (an identical question about the same page up to 1 hour old); `0` forces a fresh read of the page and a fresh answer. The response always says how old it is.
    question: str  # What to extract or answer, in plain language, e.g. "list the pricing plans with their name and monthly price in USD".
    schema: Optional[Any] = None  # Optional JSON Schema the answer must satisfy. When given, the answer is validated against it and automatically corrected where a safe fix exists (type coercion, missing defaults, out-of-range numbers, unknown properties); anything that cannot be fixed is reported in `remaining_issues`. Omitted = a free-form JSON answer, returned as-is.
    url: str  # Address of the web page to read (`http` or `https`).

    @classmethod
    def _dummy(cls) -> "GetStructuredDataRequest":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(max_age_seconds=None, question="test", schema=None, url="test")
