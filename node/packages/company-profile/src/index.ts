/**
 * Typed HTTP client and request/response interfaces for 🏢 company-profile-service.
 */

import { Client as BaseClient, type ClientOptions } from "@xyz17711/core";

export interface DomainInfo {
  /** Years since registration, one decimal. */
  domain_age_years?: number | null;
  /** Mail platform deduced from the MX records (`google-workspace`, `microsoft-365`, ...). */
  email_provider?: string | null;
  /** Expiration date, `YYYY-MM-DD`. */
  expires_at?: string | null;
  /** Sending services declared in the SPF record (`sendgrid`, `mailchimp`, ...). */
  mail_services: string[];
  nameservers: string[];
  /** Registration date, `YYYY-MM-DD`. */
  registered_at?: string | null;
  /** The registrable domain the lookups were made for. */
  registrable_domain: string;
  /** The registrant, only when it is an organization published in RDAP. */
  registrant_org?: string | null;
  registrar?: string | null;
  /** RDAP status flags (e.g. `client transfer prohibited`), at most 4. */
  statuses: string[];
}

export interface GetCompanyProfileResponse {
  /** How old this answer is, in seconds (0 for a fresh read). */
  age_seconds: number;
  /** Every automatic correction applied to the model's answer. */
  applied_fixes: unknown[];
  /** The host that was profiled, lowercased, without scheme or path. */
  domain: string;
  /** Public registration and DNS facts about the domain: registrar, registration and expiry dates, age, name servers, public registrant organization, mail platform and sending services. Fields that could not be looked up are absent or empty. */
  domain_info: DomainInfo;
  /** `true` when this answer was served from a stored result rather than a fresh read. */
  from_cache: boolean;
  /** Language of the profile's free-text values. */
  output_language: string;
  /** How many of the pages used came from a stored copy (fresh enough for `max_age_seconds`). */
  pages_from_cache: number;
  /** The pages that were actually read to build the profile. */
  pages_read: string[];
  /** Number of model passes used (2 only when the first answer was incomplete). */
  passes: number;
  /** The profile: `name`, `description`, `offering`, `target_customers`, `pricing_summary`, `headquarters`, `founded`, `contact` (`emails`, `phones`) and `social` (`linkedin`, `twitter`, `github`, `facebook`, `instagram`, `youtube`). A value the pages do not state is `null`. */
  profile: unknown;
  /** Every schema violation that could not be corrected. */
  remaining_issues: unknown[];
  /** `true` when the website was found from `company_name`. */
  resolved_from_name: boolean;
  /** When the website was read to build this profile (UTC). */
  retrieved_at: string;
  /** Language of the website (ISO 639-1 code). */
  source_language: string;
  /** How many pages could not be refreshed and were answered from an older stored copy. */
  stale_pages: number;
  /** E-mail addresses and social links the model produced that do NOT appear in the pages read; they were removed from `profile` so nothing in it is invented. */
  unverified_removed: string[];
  /** Whether the profile satisfies the profile schema after automatic correction. */
  valid?: boolean | null;
}

export interface GetCompanyProfileRequest {
  /** The company's name, when you do not know its website (e.g. `Mistral AI`): the official site is looked up first. `domain` wins when both are given. */
  company_name?: string | null;
  /** The company's website: a domain such as `stripe.com` or a full URL (`https://stripe.com/`). Give this or `company_name`. */
  domain?: string | null;
  /** Language of the free-text values of the answer (`en` by default; `fr`, `de`, `es`, `pt-BR`...). The pages may be in any language; the JSON keys are always English. */
  language?: string | null;
  /** The oldest result you accept, in seconds. Omit it for the default (profiles up to 24 hours old); `0` forces a fresh read of the website. The response always says how old it is. */
  max_age_seconds?: number | null;
}

/** Typed client for 🏢 company-profile-service, e.g. `client.getProfile(...)`. */
export class Client extends BaseClient {
  /** Company profile and enrichment from a domain or a name: offering, public contacts, social links and WHOIS domain data as valid JSON ($0.009, x402) */
  async getProfile(request: GetCompanyProfileRequest): Promise<GetCompanyProfileResponse> {
    return this.post<GetCompanyProfileResponse>("/v1/company-profile/get_profile", request);
  }
}

export { ClientOptions };
