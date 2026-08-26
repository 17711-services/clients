/**
 * Typed HTTP client and request/response interfaces for ip-blocklist.
 */

import { Client as BaseClient, type ClientOptions } from "@xyz17711/core";

export interface BlocklistMatch {
  /** The specific CIDR entry from that source that contains the queried IP. */
  cidr: string;
  /** Which source matched, e.g. `"firehol-level1"`. */
  source: string;
}

export interface CheckIpResponse {
  /** `true` if `matches` is non-empty -- a convenience flag, equivalent to `!matches.is_empty()`. */
  banned: boolean;
  ip: string;
  /** Every source that contains this IP, not just the first one found -- an IP flagged by several sources is a stronger signal than one flagged by a single list. */
  matches: BlocklistMatch[];
}

/** Typed client for ip-blocklist, e.g. `client.checkIp(...)`. */
export class Client extends BaseClient {
  /** Checks whether an IPv4 address appears on any of several public IP blocklists ($0.002, x402) */
  async checkIp(params: { ip: string }): Promise<CheckIpResponse> {
    return this.get<CheckIpResponse>("/v1/ip-blocklist/check", { ip: params.ip });
  }
}

export { ClientOptions };
