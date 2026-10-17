/**
 * Typed HTTP client and request/response interfaces for url-extract-service.
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
  /** Every automatic correction applied to the model's answer. */
  applied_fixes: unknown[];
  /** The host that was profiled, lowercased, without scheme or path. */
  domain: string;
  /** Public registration and DNS facts about the domain: registrar, registration and expiry dates, age, name servers, public registrant organization, mail platform and sending services. Fields that could not be looked up are absent or empty. */
  domain_info: DomainInfo;
  /** Language of the profile's free-text values. */
  output_language: string;
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
  /** Language of the website (ISO 639-1 code). */
  source_language: string;
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
}

export interface GetStructuredDataResponse {
  /** How old this answer is, in seconds (0 for a fresh read). */
  age_seconds: number;
  /** Every automatic correction applied to the model's answer, in order. */
  applied_fixes: unknown[];
  /** The structured answer (an object or an array), corrected against `schema` when one was given. */
  data: unknown;
  /** The URL actually read, after redirects. */
  final_url: string;
  /** `true` when this answer was served from a stored result rather than computed now. */
  from_cache: boolean;
  /** `true` when the page text came from a stored copy (fresh enough for `max_age_seconds`). */
  page_from_cache: boolean;
  /** `true` when the page was longer than the amount of text the answer is based on. */
  page_truncated: boolean;
  /** Every schema violation that could not be corrected. */
  remaining_issues: unknown[];
  /** When the page was read to build this answer (UTC). */
  retrieved_at: string;
  /** `true` when the page could not be refreshed and an older stored copy was used. */
  stale_page: boolean;
  /** The page title, when one could be extracted. */
  title?: string | null;
  /** The URL that was requested. */
  url: string;
  /** Whether `data` satisfies `schema` after correction; absent when no schema was given. */
  valid?: boolean | null;
}

export interface GetStructuredDataRequest {
  /** The oldest answer you accept, in seconds. Omit it for the default (an identical question about the same page up to 1 hour old); `0` forces a fresh read of the page and a fresh answer. The response always says how old it is. */
  max_age_seconds?: number | null;
  /** What to extract or answer, in plain language, e.g. "list the pricing plans with their name and monthly price in USD". */
  question: string;
  /** Optional JSON Schema the answer must satisfy. When given, the answer is validated against it and automatically corrected where a safe fix exists (type coercion, missing defaults, out-of-range numbers, unknown properties); anything that cannot be fixed is reported in `remaining_issues`. Omitted = a free-form JSON answer, returned as-is. */
  schema?: unknown;
  /** Address of the web page to read (`http` or `https`). */
  url: string;
}

/** Production base URL of this service; pass another to self-host or test. */
export const DEFAULT_BASE_URL = "https://api.17711.xyz/registry/url-extract-service";

/** Typed client for url-extract-service, e.g. `client.getCompanyProfile(...)`. */
export class Client extends BaseClient {
  /**
   * `new Client()` talks to the production service. Pass a base URL to target another
   * instance, and/or wallet options (`new Client({ x402PrivateKey, ... })`) to pay past the
   * free quota automatically.
   */
  constructor(options?: ClientOptions);
  constructor(baseUrl?: string, options?: ClientOptions);
  constructor(baseUrlOrOptions?: string | ClientOptions, options: ClientOptions = {}) {
    const [url, opts]: [string, ClientOptions] =
      typeof baseUrlOrOptions === "object"
        ? [DEFAULT_BASE_URL, baseUrlOrOptions]
        : [baseUrlOrOptions ?? DEFAULT_BASE_URL, options];
    super(url, opts);
  }

  /** [Deprecated - use company_profile_get_profile] Company profile from a domain or a name as valid JSON ($0.009, x402) */
  async getCompanyProfile(request: GetCompanyProfileRequest): Promise<GetCompanyProfileResponse> {
    return this.post<GetCompanyProfileResponse>("/v1/url-extract/get_company_profile", request);
  }

  /** URL extract with a question: ask any web page a question and get structured data as JSON that matches your schema ($0.02, x402) */
  async getStructuredData(request: GetStructuredDataRequest): Promise<GetStructuredDataResponse> {
    return this.post<GetStructuredDataResponse>("/v1/url-extract/get_structured_data", request);
  }
}

export { ClientOptions };
