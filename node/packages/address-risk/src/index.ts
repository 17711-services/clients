/**
 * Typed HTTP client and request/response interfaces for address-risk-service.
 */

import { Client as BaseClient, type ClientOptions } from "@xyz17711/core";

export interface Flag {
  /** Stable code, e.g. `sanctioned`, `phishing`, `theft`, `mixer`, `blacklist_doubt`. */
  code: string;
  message: string;
  /** `critical`, `high` or `medium`. */
  severity: string;
}

export interface CheckAddressResponse {
  address: string;
  /** How old this result is, in seconds (0 for a fresh check). */
  age_seconds: number;
  chain: string;
  disclaimer: string;
  /** Every flag raised, most severe first. Empty when the verdict is `clear`. */
  flags: Flag[];
  /** `true` when served from a stored result. */
  from_cache: boolean;
  /** `contract` or `wallet`. */
  kind: string;
  /** Who reported the address, when the source says (e.g. `SlowMist,BlockSec`). */
  reported_by?: string | null;
  /** When the data was read (UTC). */
  retrieved_at: string;
  /** 0 to 100, higher is safer; derived from the flags. */
  safety_score: number;
  /** `clear` (no known flag), `caution`, `risky` or `dangerous`. `clear` means no report was found, not that the address is guaranteed safe. */
  verdict: string;
}

export interface CheckAddressRequest {
  /** The wallet or contract address to screen (`0x` followed by 40 hex characters). */
  address: string;
  /** The chain: `base` (default), `ethereum`, `bsc`, `polygon`, `arbitrum`, `optimism` or `avalanche`. */
  chain?: string | null;
  /** The oldest result you accept, in seconds. Omit it for the default (up to 10 minutes old); `0` forces a fresh check. The response always says how old it is. */
  max_age_seconds?: number | null;
}

/** Typed client for address-risk-service, e.g. `client.checkAddress(...)`. */
export class Client extends BaseClient {
  /** Wallet address risk check: sanctioned address and phishing check for a crypto wallet or contract before you send funds, with theft, scam, mixer and blacklist flags ($0.005, x402) */
  async checkAddress(request: CheckAddressRequest): Promise<CheckAddressResponse> {
    return this.post<CheckAddressResponse>("/v1/address-risk/check_address", request);
  }
}

export { ClientOptions };
