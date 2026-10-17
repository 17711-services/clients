/**
 * Typed HTTP client and request/response interfaces for contact-finder-service.
 */

import { Client as BaseClient, type ClientOptions } from "@xyz17711/core";

export interface Contact {
  /** `high` (published as a link or in structured data), `medium` or `low`. */
  confidence: string;
  /** How it appears there: `mailto`, `text`, `jsonld`, `tel`, `form`, `link`, `probe` (a common address that exists), `security.txt`. */
  found_in: string;
  /** `email`, `phone`, `form` (a contact form), `page` (a contact, support or help-centre page), `messaging` (WhatsApp, Telegram, Signal, Messenger), `security` (a vulnerability-reporting contact) or `social` (a profile link). */
  kind: string;
  /** The label published next to it (link text or heading), when there is one. */
  label?: string | null;
  /** For an e-mail address: whether its domain has mail servers (`false` = it cannot receive mail). */
  mx_valid?: boolean | null;
  /** `sales`, `support`, `press`, `jobs`, `legal`, `privacy`, `security`, `billing` or `general`. */
  role: string;
  /** The page where it was found. */
  source_url: string;
  /** The address, number or link, exactly as published. */
  value: string;
}

export interface DomainMail {
  /** DMARC policy: `reject`, `quarantine`, `none` or `absent`. */
  dmarc?: string | null;
  /** Mail servers (MX) of the website's domain, highest priority first (at most 5). */
  mx: string[];
  /** Mail platform deduced from the MX records (`google-workspace`, `microsoft-365`, ...). */
  provider?: string | null;
  /** SPF policy: `strict` (-all), `soft` (~all), `neutral` (?all), `open` (+all) or `none`. */
  spf?: string | null;
}

export interface GetContactsResponse {
  /** How old this answer is, in seconds (0 for a fresh read). */
  age_seconds: number;
  /** Public business contacts: role mailboxes, phones, contact forms, messaging links, security contact and social profiles -- only what is literally published on the pages read. */
  contacts: Contact[];
  /** The host that was searched, lowercased, without scheme or path. */
  domain: string;
  /** Mail health of the website's own domain: mail servers, platform, SPF and DMARC policies. */
  domain_mail: DomainMail;
  /** `true` when this answer was served from a stored result rather than a fresh read. */
  from_cache: boolean;
  /** Whether a contact form was found. */
  has_contact_form: boolean;
  /** E-mail addresses that look personal (a named individual) or have no recognizable role: they are not returned, only counted. */
  omitted_non_role_addresses: number;
  /** How many of the pages used came from a stored copy (fresh enough for `max_age_seconds`). */
  pages_from_cache: number;
  /** The pages that were actually read. */
  pages_read: string[];
  /** `true` when the website was found from `company_name`. */
  resolved_from_name: boolean;
  /** When the website was read to build this list (UTC). */
  retrieved_at: string;
  /** The first security contact published (security.txt), when there is one. */
  security_contact?: string | null;
  /** Language of the website (ISO 639-1 code). */
  source_language: string;
  /** How many pages could not be refreshed and were answered from an older stored copy. */
  stale_pages: number;
}

export interface GetContactsRequest {
  /** The company's name, when you do not know its website (e.g. `Mistral AI`): the official site is looked up first. `domain` wins when both are given. */
  company_name?: string | null;
  /** The company's website: a domain such as `stripe.com` or a full URL (`https://stripe.com/`). Give this or `company_name`. */
  domain?: string | null;
  /** The oldest result you accept, in seconds. Omit it for the default (results up to 12 hours old); `0` forces a fresh read of the website. The response always says how old it is. */
  max_age_seconds?: number | null;
}

/** Typed client for contact-finder-service, e.g. `client.getContacts(...)`. */
export class Client extends BaseClient {
  /** Contact finder: public business emails, phone numbers, contact forms and support pages of a domain, with role and source ($0.009, x402) */
  async getContacts(request: GetContactsRequest): Promise<GetContactsResponse> {
    return this.post<GetContactsResponse>("/v1/contact-finder/get_contacts", request);
  }
}

export { ClientOptions };
