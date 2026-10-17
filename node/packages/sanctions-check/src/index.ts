/**
 * Typed HTTP client and request/response interfaces for 🚫 sanctions-check-service.
 */

import { Client as BaseClient, type ClientOptions } from "@xyz17711/core";

export interface ListStatus {
  entries: number;
  /** When this service last downloaded the list (UTC). */
  fetched_at: string;
  list: string;
  /** Publication date announced by the list itself, when it states one. */
  published?: string | null;
}

export interface SanctionMatch {
  /** Other names the entry is listed under (at most 5). */
  aliases: string[];
  /** `true`/`false` when a `birth_year` was given and the entry publishes birth years. */
  birth_year_consistent?: boolean | null;
  /** Published years of birth. */
  birth_years: number[];
  /** Nationalities or countries, when published. */
  countries: string[];
  /** The entry's identifier in that list. */
  entry_id: string;
  /** `person`, `entity`, `vessel` or `aircraft`. */
  kind: string;
  /** `OFAC SDN`, `EU consolidated` or `UN Security Council`. */
  list: string;
  /** The listed primary name. */
  listed_name: string;
  /** Date of listing, when published. */
  listed_on?: string | null;
  /** `exact`, `close` or `possible`. */
  match_type: string;
  /** The name or alias that matched, when it is not the primary name. */
  matched_alias?: string | null;
  /** Sanctions programmes or regimes. */
  programs: string[];
  /** Published remarks (truncated). */
  remarks?: string | null;
  /** 0 to 1: 1 means the same words (any order); lower means a partial or approximate match. */
  score: number;
}

export interface ScreenNameResponse {
  disclaimer: string;
  /** Lists that could not be loaded: the screening did not cover them. */
  lists_missing: string[];
  /** The lists that were screened, with their size and freshness. */
  lists_screened: ListStatus[];
  /** The best matches, highest score first (at most 10). */
  matches: SanctionMatch[];
  /** The name as screened. */
  name: string;
  /** When the screening ran (UTC). */
  screened_at: string;
  /** `match` (an exact or close match), `possible_match` (a partial match to review) or `no_match`. */
  verdict: string;
}

export interface ScreenNameRequest {
  /** A person's year of birth. Listed people whose published birth years do not include it are ranked lower and marked `birth_year_consistent: false`. */
  birth_year?: number | null;
  /** The name to screen: a person (`Vladimir Putin`, `Putin, Vladimir`) or a company, vessel or organisation. Word order, accents, capitalisation and small spelling variants do not matter. */
  name: string;
  /** Restrict the screening to `person`, `entity`, `vessel` or `aircraft`. Omit it to screen everything. */
  type?: string | null;
}

/** Typed client for 🚫 sanctions-check-service, e.g. `client.screenName(...)`. */
export class Client extends BaseClient {
  /** Sanctions check: OFAC list check and sanctions screening of a person or company name against OFAC SDN, EU and UN lists (AML KYC) ($0.01, x402) */
  async screenName(request: ScreenNameRequest): Promise<ScreenNameResponse> {
    return this.post<ScreenNameResponse>("/v1/sanctions-check/screen_name", request);
  }
}

export { ClientOptions };
