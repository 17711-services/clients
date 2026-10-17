/**
 * Typed HTTP client and request/response interfaces for company-check-service.
 */

import { Client as BaseClient, type ClientOptions } from "@xyz17711/core";

export interface Company {
  /** Main activity code (NAF/APE for France). */
  activity_code?: string | null;
  address?: string | null;
  /** Date of closure (YYYY-MM-DD), when closed. */
  closed_at?: string | null;
  /** ISO country code of the legal seat. */
  country: string;
  /** Date of creation (YYYY-MM-DD). */
  created_at?: string | null;
  /** Employee size bracket, e.g. `50-99`. */
  employees?: string | null;
  /** SIRET of the head office (France). */
  head_office_id?: string | null;
  /** Legal form (`SAS`, `SARL`, ...) or its register code. */
  legal_form?: string | null;
  legal_name: string;
  lei?: string | null;
  /** Number in the company register (SIREN for France). */
  registration_number?: string | null;
  /** Size category: `PME`, `ETI`, `GE`. */
  size_category?: string | null;
  /** `active`, `closed` or `unknown`. */
  status: string;
  /** Commercial name or acronym, when different. */
  trade_name?: string | null;
  vat_number?: string | null;
}

export interface Director {
  /** Month and year of birth (`1975-01`) for a person, as published in the register. */
  born?: string | null;
  /** `person` or `company`. */
  kind: string;
  /** Full name of the person or the legal entity. */
  name: string;
  nationality?: string | null;
  /** Registration number of a legal-entity director. */
  registration_number?: string | null;
  /** Role as published (`Président de SAS`, `Directeur Général`, `Commissaire aux comptes titulaire`...). */
  role: string;
}

export interface Financial {
  /** Net result, in euros. */
  net_result?: number | null;
  /** Revenue, in euros. */
  revenue?: number | null;
  year: number;
}

export interface Flag {
  /** Stable code, e.g. `company.closed`, `vat.invalid`, `vat.name_mismatch`, `lei.lapsed`. */
  code: string;
  message: string;
  /** `high`, `medium`, `low` or `info`. */
  severity: string;
}

export interface LeiParent {
  country?: string | null;
  legal_name: string;
  lei: string;
}

export interface LeiRecord {
  direct_parent?: LeiParent | null;
  /** Entity status in the LEI register (`ACTIVE`, `INACTIVE`). */
  entity_status: string;
  lei: string;
  next_renewal?: string | null;
  /** Registration status of the LEI (`ISSUED`, `LAPSED`, ...). */
  registration_status: string;
  ultimate_parent?: LeiParent | null;
}

export interface Candidate {
  city?: string | null;
  name: string;
  registration_number: string;
  status: string;
}

export interface VatCheck {
  /** When the number was validated (UTC). */
  checked_at: string;
  /** The number as checked, with country prefix. */
  number: string;
  registered_address?: string | null;
  /** Name registered for the VAT number, when the member state discloses it. */
  registered_name?: string | null;
  /** `valid`, `invalid` or `unavailable` (the EU service did not answer: try again later). */
  status: string;
}

export interface VerifyCompanyResponse {
  /** How old this answer is, in seconds (0 for a fresh check). */
  age_seconds: number;
  company: Company;
  /** `high` (identified by a number), `medium` (a clear name match) or `low` (several similar names). */
  confidence: string;
  /** What this answer does not cover for the company's country. */
  coverage_note: string;
  /** Officers and statutory auditors published in the register (France only). */
  directors: Director[];
  /** Revenue and net result of the latest published years (France only). */
  financials: Financial[];
  /** Things to know: closed company, invalid VAT number, name mismatch, lapsed LEI. */
  flags: Flag[];
  /** `true` when this answer was served from a stored result. */
  from_cache: boolean;
  lei?: LeiRecord | null;
  /** How the company was identified: `lei`, `vat_number`, `registration_number` or `name`. */
  matched_by: string;
  /** Other companies that matched a name search (to disambiguate). */
  other_candidates: Candidate[];
  /** When the registers were queried (UTC). */
  retrieved_at: string;
  /** The registers consulted. */
  sources: string[];
  /** VAT number validation, when a VAT number is known. */
  vat?: VatCheck | null;
}

export interface VerifyCompanyRequest {
  /** The company's name (`OVH`, `Mistral AI`). Give at least one of `company_name`, `registration_number`, `vat_number` or `lei`. */
  company_name?: string | null;
  /** ISO 3166-1 alpha-2 country code (`FR`, `DE`) to narrow a name or number search. */
  country?: string | null;
  /** A Legal Entity Identifier (20 characters). */
  lei?: string | null;
  /** The oldest answer you accept, in seconds. Omit it for the default (answers up to 6 hours old); `0` forces a fresh check, including a new VAT validation. */
  max_age_seconds?: number | null;
  /** A company registration number: a French SIREN (9 digits) or SIRET (14 digits), or a number from another register (then give `country`). */
  registration_number?: string | null;
  /** An EU VAT number with its country prefix (`FR22424761419`, `DE811907980`). */
  vat_number?: string | null;
}

/** Production base URL of this service; pass another to self-host or test. */
export const DEFAULT_BASE_URL = "https://api.17711.xyz/registry/company-check-service";

/** Typed client for company-check-service, e.g. `client.verifyCompany(...)`. */
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

  /** Company check (KYB) and business verification: VAT validation (VIES), LEI lookup, registry status and company directors ($0.009, x402) */
  async verifyCompany(request: VerifyCompanyRequest): Promise<VerifyCompanyResponse> {
    return this.post<VerifyCompanyResponse>("/v1/company-check/verify_company", request);
  }
}

export { ClientOptions };
