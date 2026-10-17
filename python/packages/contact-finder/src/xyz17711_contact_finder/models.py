"""Pydantic request/response models for 📇 contact-finder-service."""

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class Contact(BaseModel):
    confidence: str  # `high` (published as a link or in structured data), `medium` or `low`.
    found_in: str  # How it appears there: `mailto`, `text`, `jsonld`, `tel`, `form`, `link`, `probe` (a common address that exists), `security.txt`.
    kind: str  # `email`, `phone`, `form` (a contact form), `page` (a contact, support or help-centre page), `messaging` (WhatsApp, Telegram, Signal, Messenger), `security` (a vulnerability-reporting contact) or `social` (a profile link).
    label: Optional[str] = None  # The label published next to it (link text or heading), when there is one.
    mx_valid: Optional[bool] = None  # For an e-mail address: whether its domain has mail servers (`false` = it cannot receive mail).
    role: str  # `sales`, `support`, `press`, `jobs`, `legal`, `privacy`, `security`, `billing` or `general`.
    source_url: str  # The page where it was found.
    value: str  # The address, number or link, exactly as published.

    @classmethod
    def _dummy(cls) -> "Contact":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(confidence="test", found_in="test", kind="test", label=None, mx_valid=None, role="test", source_url="test", value="test")


class DomainMail(BaseModel):
    dmarc: Optional[str] = None  # DMARC policy: `reject`, `quarantine`, `none` or `absent`.
    mx: List[str]  # Mail servers (MX) of the website's domain, highest priority first (at most 5).
    provider: Optional[str] = None  # Mail platform deduced from the MX records (`google-workspace`, `microsoft-365`, ...).
    spf: Optional[str] = None  # SPF policy: `strict` (-all), `soft` (~all), `neutral` (?all), `open` (+all) or `none`.

    @classmethod
    def _dummy(cls) -> "DomainMail":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(dmarc=None, mx=[], provider=None, spf=None)


class GetContactsResponse(BaseModel):
    age_seconds: int  # How old this answer is, in seconds (0 for a fresh read).
    contacts: List[Contact]  # Public business contacts: role mailboxes, phones, contact forms, messaging links, security contact and social profiles -- only what is literally published on the pages read.
    domain: str  # The host that was searched, lowercased, without scheme or path.
    domain_mail: DomainMail  # Mail health of the website's own domain: mail servers, platform, SPF and DMARC policies.
    from_cache: bool  # `true` when this answer was served from a stored result rather than a fresh read.
    has_contact_form: bool  # Whether a contact form was found.
    omitted_non_role_addresses: int  # E-mail addresses that look personal (a named individual) or have no recognizable role: they are not returned, only counted.
    pages_from_cache: int  # How many of the pages used came from a stored copy (fresh enough for `max_age_seconds`).
    pages_read: List[str]  # The pages that were actually read.
    resolved_from_name: bool  # `true` when the website was found from `company_name`.
    retrieved_at: str  # When the website was read to build this list (UTC).
    security_contact: Optional[str] = None  # The first security contact published (security.txt), when there is one.
    source_language: str  # Language of the website (ISO 639-1 code).
    stale_pages: int  # How many pages could not be refreshed and were answered from an older stored copy.

    @classmethod
    def _dummy(cls) -> "GetContactsResponse":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(age_seconds=0, contacts=[], domain="test", domain_mail=DomainMail._dummy(), from_cache=False, has_contact_form=False, omitted_non_role_addresses=0, pages_from_cache=0, pages_read=[], resolved_from_name=False, retrieved_at="test", security_contact=None, source_language="test", stale_pages=0)


class GetContactsRequest(BaseModel):
    company_name: Optional[str] = None  # The company's name, when you do not know its website (e.g. `Mistral AI`): the official site is looked up first. `domain` wins when both are given.
    domain: Optional[str] = None  # The company's website: a domain such as `stripe.com` or a full URL (`https://stripe.com/`). Give this or `company_name`.
    max_age_seconds: Optional[int] = None  # The oldest result you accept, in seconds. Omit it for the default (results up to 12 hours old); `0` forces a fresh read of the website. The response always says how old it is.

    @classmethod
    def _dummy(cls) -> "GetContactsRequest":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(company_name=None, domain=None, max_age_seconds=None)
