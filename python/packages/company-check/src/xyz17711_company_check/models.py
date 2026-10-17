"""Pydantic request/response models for company-check-service."""

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class Company(BaseModel):
    activity_code: Optional[str] = None  # Main activity code (NAF/APE for France).
    address: Optional[str] = None
    closed_at: Optional[str] = None  # Date of closure (YYYY-MM-DD), when closed.
    country: str  # ISO country code of the legal seat.
    created_at: Optional[str] = None  # Date of creation (YYYY-MM-DD).
    employees: Optional[str] = None  # Employee size bracket, e.g. `50-99`.
    head_office_id: Optional[str] = None  # SIRET of the head office (France).
    legal_form: Optional[str] = None  # Legal form (`SAS`, `SARL`, ...) or its register code.
    legal_name: str
    lei: Optional[str] = None
    registration_number: Optional[str] = None  # Number in the company register (SIREN for France).
    size_category: Optional[str] = None  # Size category: `PME`, `ETI`, `GE`.
    status: str  # `active`, `closed` or `unknown`.
    trade_name: Optional[str] = None  # Commercial name or acronym, when different.
    vat_number: Optional[str] = None

    @classmethod
    def _dummy(cls) -> "Company":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(activity_code=None, address=None, closed_at=None, country="test", created_at=None, employees=None, head_office_id=None, legal_form=None, legal_name="test", lei=None, registration_number=None, size_category=None, status="test", trade_name=None, vat_number=None)


class Director(BaseModel):
    born: Optional[str] = None  # Month and year of birth (`1975-01`) for a person, as published in the register.
    kind: str  # `person` or `company`.
    name: str  # Full name of the person or the legal entity.
    nationality: Optional[str] = None
    registration_number: Optional[str] = None  # Registration number of a legal-entity director.
    role: str  # Role as published (`Président de SAS`, `Directeur Général`, `Commissaire aux comptes titulaire`...).

    @classmethod
    def _dummy(cls) -> "Director":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(born=None, kind="test", name="test", nationality=None, registration_number=None, role="test")


class Financial(BaseModel):
    net_result: Optional[int] = None  # Net result, in euros.
    revenue: Optional[int] = None  # Revenue, in euros.
    year: int

    @classmethod
    def _dummy(cls) -> "Financial":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(net_result=None, revenue=None, year=0)


class Flag(BaseModel):
    code: str  # Stable code, e.g. `company.closed`, `vat.invalid`, `vat.name_mismatch`, `lei.lapsed`.
    message: str
    severity: str  # `high`, `medium`, `low` or `info`.

    @classmethod
    def _dummy(cls) -> "Flag":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(code="test", message="test", severity="test")


class LeiParent(BaseModel):
    country: Optional[str] = None
    legal_name: str
    lei: str

    @classmethod
    def _dummy(cls) -> "LeiParent":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(country=None, legal_name="test", lei="test")


class LeiRecord(BaseModel):
    direct_parent: Optional[LeiParent] = None
    entity_status: str  # Entity status in the LEI register (`ACTIVE`, `INACTIVE`).
    lei: str
    next_renewal: Optional[str] = None
    registration_status: str  # Registration status of the LEI (`ISSUED`, `LAPSED`, ...).
    ultimate_parent: Optional[LeiParent] = None

    @classmethod
    def _dummy(cls) -> "LeiRecord":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(direct_parent=None, entity_status="test", lei="test", next_renewal=None, registration_status="test", ultimate_parent=None)


class Candidate(BaseModel):
    city: Optional[str] = None
    name: str
    registration_number: str
    status: str

    @classmethod
    def _dummy(cls) -> "Candidate":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(city=None, name="test", registration_number="test", status="test")


class VatCheck(BaseModel):
    checked_at: str  # When the number was validated (UTC).
    number: str  # The number as checked, with country prefix.
    registered_address: Optional[str] = None
    registered_name: Optional[str] = None  # Name registered for the VAT number, when the member state discloses it.
    status: str  # `valid`, `invalid` or `unavailable` (the EU service did not answer: try again later).

    @classmethod
    def _dummy(cls) -> "VatCheck":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(checked_at="test", number="test", registered_address=None, registered_name=None, status="test")


class VerifyCompanyResponse(BaseModel):
    age_seconds: int  # How old this answer is, in seconds (0 for a fresh check).
    company: Company
    confidence: str  # `high` (identified by a number), `medium` (a clear name match) or `low` (several similar names).
    coverage_note: str  # What this answer does not cover for the company's country.
    directors: List[Director]  # Officers and statutory auditors published in the register (France only).
    financials: List[Financial]  # Revenue and net result of the latest published years (France only).
    flags: List[Flag]  # Things to know: closed company, invalid VAT number, name mismatch, lapsed LEI.
    from_cache: bool  # `true` when this answer was served from a stored result.
    lei: Optional[LeiRecord] = None
    matched_by: str  # How the company was identified: `lei`, `vat_number`, `registration_number` or `name`.
    other_candidates: List[Candidate]  # Other companies that matched a name search (to disambiguate).
    retrieved_at: str  # When the registers were queried (UTC).
    sources: List[str]  # The registers consulted.
    vat: Optional[VatCheck] = None  # VAT number validation, when a VAT number is known.

    @classmethod
    def _dummy(cls) -> "VerifyCompanyResponse":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(age_seconds=0, company=Company._dummy(), confidence="test", coverage_note="test", directors=[], financials=[], flags=[], from_cache=False, lei=None, matched_by="test", other_candidates=[], retrieved_at="test", sources=[], vat=None)


class VerifyCompanyRequest(BaseModel):
    company_name: Optional[str] = None  # The company's name (`OVH`, `Mistral AI`). Give at least one of `company_name`, `registration_number`, `vat_number` or `lei`.
    country: Optional[str] = None  # ISO 3166-1 alpha-2 country code (`FR`, `DE`) to narrow a name or number search.
    lei: Optional[str] = None  # A Legal Entity Identifier (20 characters).
    max_age_seconds: Optional[int] = None  # The oldest answer you accept, in seconds. Omit it for the default (answers up to 6 hours old); `0` forces a fresh check, including a new VAT validation.
    registration_number: Optional[str] = None  # A company registration number: a French SIREN (9 digits) or SIRET (14 digits), or a number from another register (then give `country`).
    vat_number: Optional[str] = None  # An EU VAT number with its country prefix (`FR22424761419`, `DE811907980`).

    @classmethod
    def _dummy(cls) -> "VerifyCompanyRequest":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(company_name=None, country=None, lei=None, max_age_seconds=None, registration_number=None, vat_number=None)
