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

/** Production base URL of this service; pass another to self-host or test. */
export const DEFAULT_BASE_URL = "https://api.17711.xyz/registry/ip-blocklist";

/** Typed client for ip-blocklist, e.g. `client.checkIp(...)`. */
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

  /** IP reputation check: is this IPv4 address on a public threat blocklist (Tor exit nodes, botnets, spam networks) ($0.010, x402) */
  async checkIp(params: { ip: string }): Promise<CheckIpResponse> {
    return this.get<CheckIpResponse>("/v1/ip-blocklist/check", { ip: params.ip });
  }
}

export { ClientOptions };
