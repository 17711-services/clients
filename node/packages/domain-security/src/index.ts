/**
 * Typed HTTP client and request/response interfaces for 🛡️ domain-security-service.
 */

import { Client as BaseClient, type ClientOptions } from "@xyz17711/core";

export interface BlocklistHit {
  cidr: string;
  ip: string;
  source: string;
}

export interface DnsSecurity {
  /** CAA records: the certificate authorities allowed to issue for the domain. */
  caa: string[];
  /** Whether the answer for the domain is validated by DNSSEC. */
  dnssec: boolean;
  /** Authoritative name servers (at most 8). */
  name_servers: string[];
}

export interface Finding {
  /** Stable machine-readable code, e.g. `tls.expired`, `mail.dmarc_absent`, `http.hsts_missing`. */
  code: string;
  /** What was observed and why it matters, in one sentence. */
  message: string;
  /** `critical`, `high`, `medium`, `low` or `info`. */
  severity: string;
}

export interface HttpSecurity {
  /** Whether the `Server` / `X-Powered-By` headers disclose a software version. */
  discloses_version: boolean;
  /** The ones that are missing. */
  headers_missing: string[];
  /** Security headers found on the HTTPS response (`strict-transport-security`, `content-security-policy`, `x-content-type-options`, `x-frame-options`, `referrer-policy`, `permissions-policy`). */
  headers_present: string[];
  /** `true` when plain HTTP on port 80 redirects to HTTPS, `false` when it serves content or redirects elsewhere, absent when port 80 does not answer. */
  http_redirects_to_https?: boolean | null;
  /** Status of `GET https://<domain>/`. */
  https_status?: number | null;
}

export interface MailSecurity {
  /** DMARC policy: `reject`, `quarantine`, `none` or `absent`. */
  dmarc?: string | null;
  /** Whether an MTA-STS policy is published (`_mta-sts` TXT record). */
  mta_sts: boolean;
  /** Mail servers (MX) of the website's domain, highest priority first (at most 5). */
  mx: string[];
  /** Mail platform deduced from the MX records (`google-workspace`, `microsoft-365`, ...). */
  provider?: string | null;
  /** SPF policy: `strict` (-all), `soft` (~all), `neutral` (?all), `open` (+all) or `none`. */
  spf?: string | null;
}

export interface TlsSecurity {
  /** Days left before expiry (negative once expired). */
  days_remaining?: number | null;
  /** Why the handshake or validation failed, when it did. */
  error?: string | null;
  /** Certificate end of validity (UTC). */
  expires_at?: string | null;
  issuer?: string | null;
  /** `TLS1.3` or `TLS1.2`. */
  protocol?: string | null;
  /** Whether HTTPS answered on port 443. */
  reachable: boolean;
  /** Number of host names the certificate covers. */
  san_count: number;
  /** Whether the certificate chain validates for this host name. */
  valid: boolean;
}

export interface GetReportResponse {
  /** How old this report is, in seconds (0 for a fresh assessment). */
  age_seconds: number;
  /** Addresses found on a public IP blocklist (IPv4 only). */
  blocklisted: BlocklistHit[];
  dns: DnsSecurity;
  /** The host that was assessed, lowercased, without scheme or path. */
  domain: string;
  /** Everything worth acting on, most severe first. */
  findings: Finding[];
  /** `true` when this report was served from a stored result. */
  from_cache: boolean;
  /** `A` (90+), `B` (80+), `C` (65+), `D` (50+), `F`. */
  grade: string;
  http: HttpSecurity;
  /** Public IPv4/IPv6 addresses of the host (at most 8). */
  ip_addresses: string[];
  mail: MailSecurity;
  /** When the assessment was made (UTC). */
  retrieved_at: string;
  /** 0 to 100, higher is better; derived from the findings. */
  score: number;
  tls: TlsSecurity;
}

export interface GetReportRequest {
  /** The domain to assess: `stripe.com`, `www.stripe.com` or a full URL (only the host is used). */
  domain: string;
  /** The oldest report you accept, in seconds. Omit it for the default (reports up to 1 hour old); `0` forces a fresh assessment. The response always says how old it is. */
  max_age_seconds?: number | null;
}

/** Typed client for 🛡️ domain-security-service, e.g. `client.getReport(...)`. */
export class Client extends BaseClient {
  /** Domain security check: SSL certificate check, DMARC SPF check, DNSSEC, security headers and blocklist status with a score ($0.009, x402) */
  async getReport(request: GetReportRequest): Promise<GetReportResponse> {
    return this.post<GetReportResponse>("/v1/domain-security/get_report", request);
  }
}

export { ClientOptions };
