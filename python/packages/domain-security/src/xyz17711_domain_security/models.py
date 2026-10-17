"""Pydantic request/response models for 🛡️ domain-security-service."""

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class BlocklistHit(BaseModel):
    cidr: str
    ip: str
    source: str

    @classmethod
    def _dummy(cls) -> "BlocklistHit":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(cidr="test", ip="test", source="test")


class DnsSecurity(BaseModel):
    caa: List[str]  # CAA records: the certificate authorities allowed to issue for the domain.
    dnssec: bool  # Whether the answer for the domain is validated by DNSSEC.
    name_servers: List[str]  # Authoritative name servers (at most 8).

    @classmethod
    def _dummy(cls) -> "DnsSecurity":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(caa=[], dnssec=False, name_servers=[])


class Finding(BaseModel):
    code: str  # Stable machine-readable code, e.g. `tls.expired`, `mail.dmarc_absent`, `http.hsts_missing`.
    message: str  # What was observed and why it matters, in one sentence.
    severity: str  # `critical`, `high`, `medium`, `low` or `info`.

    @classmethod
    def _dummy(cls) -> "Finding":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(code="test", message="test", severity="test")


class HttpSecurity(BaseModel):
    discloses_version: bool  # Whether the `Server` / `X-Powered-By` headers disclose a software version.
    headers_missing: List[str]  # The ones that are missing.
    headers_present: List[str]  # Security headers found on the HTTPS response (`strict-transport-security`, `content-security-policy`, `x-content-type-options`, `x-frame-options`, `referrer-policy`, `permissions-policy`).
    http_redirects_to_https: Optional[bool] = None  # `true` when plain HTTP on port 80 redirects to HTTPS, `false` when it serves content or redirects elsewhere, absent when port 80 does not answer.
    https_status: Optional[int] = None  # Status of `GET https://<domain>/`.

    @classmethod
    def _dummy(cls) -> "HttpSecurity":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(discloses_version=False, headers_missing=[], headers_present=[], http_redirects_to_https=None, https_status=None)


class MailSecurity(BaseModel):
    dmarc: Optional[str] = None  # DMARC policy: `reject`, `quarantine`, `none` or `absent`.
    mta_sts: bool  # Whether an MTA-STS policy is published (`_mta-sts` TXT record).
    mx: List[str]  # Mail servers (MX) of the website's domain, highest priority first (at most 5).
    provider: Optional[str] = None  # Mail platform deduced from the MX records (`google-workspace`, `microsoft-365`, ...).
    spf: Optional[str] = None  # SPF policy: `strict` (-all), `soft` (~all), `neutral` (?all), `open` (+all) or `none`.

    @classmethod
    def _dummy(cls) -> "MailSecurity":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(dmarc=None, mta_sts=False, mx=[], provider=None, spf=None)


class TlsSecurity(BaseModel):
    days_remaining: Optional[int] = None  # Days left before expiry (negative once expired).
    error: Optional[str] = None  # Why the handshake or validation failed, when it did.
    expires_at: Optional[str] = None  # Certificate end of validity (UTC).
    issuer: Optional[str] = None
    protocol: Optional[str] = None  # `TLS1.3` or `TLS1.2`.
    reachable: bool  # Whether HTTPS answered on port 443.
    san_count: int  # Number of host names the certificate covers.
    valid: bool  # Whether the certificate chain validates for this host name.

    @classmethod
    def _dummy(cls) -> "TlsSecurity":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(days_remaining=None, error=None, expires_at=None, issuer=None, protocol=None, reachable=False, san_count=0, valid=False)


class GetReportResponse(BaseModel):
    age_seconds: int  # How old this report is, in seconds (0 for a fresh assessment).
    blocklisted: List[BlocklistHit]  # Addresses found on a public IP blocklist (IPv4 only).
    dns: DnsSecurity
    domain: str  # The host that was assessed, lowercased, without scheme or path.
    findings: List[Finding]  # Everything worth acting on, most severe first.
    from_cache: bool  # `true` when this report was served from a stored result.
    grade: str  # `A` (90+), `B` (80+), `C` (65+), `D` (50+), `F`.
    http: HttpSecurity
    ip_addresses: List[str]  # Public IPv4/IPv6 addresses of the host (at most 8).
    mail: MailSecurity
    retrieved_at: str  # When the assessment was made (UTC).
    score: int  # 0 to 100, higher is better; derived from the findings.
    tls: TlsSecurity

    @classmethod
    def _dummy(cls) -> "GetReportResponse":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(age_seconds=0, blocklisted=[], dns=DnsSecurity._dummy(), domain="test", findings=[], from_cache=False, grade="test", http=HttpSecurity._dummy(), ip_addresses=[], mail=MailSecurity._dummy(), retrieved_at="test", score=0, tls=TlsSecurity._dummy())


class GetReportRequest(BaseModel):
    domain: str  # The domain to assess: `stripe.com`, `www.stripe.com` or a full URL (only the host is used).
    max_age_seconds: Optional[int] = None  # The oldest report you accept, in seconds. Omit it for the default (reports up to 1 hour old); `0` forces a fresh assessment. The response always says how old it is.

    @classmethod
    def _dummy(cls) -> "GetReportRequest":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(domain="test", max_age_seconds=None)
