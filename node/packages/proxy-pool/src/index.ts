/**
 * Typed HTTP client and request/response interfaces for proxy-pool.
 */

import { Client as BaseClient, type ClientOptions } from "@xyz17711/core";

/** A `SourceProxy` joined with its `CheckedProxy` result, if it has been checked at least once -- what every read tool actually filters/returns. */
export interface ProxyView {
  anonymity: string;
  /** `None` if this service has never checked this proxy yet. */
  checked_alive?: boolean | null;
  checked_at?: number | null;
  /** See `CheckedProxy::consecutive_successes`'s own doc comment. `0` if never checked. */
  checked_consecutive_successes: number;
  /** See `CheckedProxy::ema_latency_ms`'s own doc comment. */
  checked_ema_latency_ms?: number | null;
  checked_latency_ms?: number | null;
  checked_protocol?: string | null;
  city: string;
  country: string;
  id: string;
  ip: string;
  port: number;
  protocols: string[];
}

export interface GetBestProxyResponse {
  proxy: ProxyView;
}

/** Production base URL of this service; pass another to self-host or test. */
export const DEFAULT_BASE_URL = "https://api.17711.xyz/registry/proxy-pool";

/** Typed client for proxy-pool, e.g. `client.getBestProxy(...)`. */
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

  /** Free proxy API: get one fast, verified-alive proxy (HTTP, SOCKS) filtered by country, protocol and anonymity, for scraping ($0.010, x402) */
  async getBestProxy(params: { anonymity?: string | null; city?: string | null; country?: string | null; protocol?: string | null }): Promise<GetBestProxyResponse> {
    return this.get<GetBestProxyResponse>("/v1/proxy-pool/get_best_proxy", { anonymity: params.anonymity, city: params.city, country: params.country, protocol: params.protocol });
  }
}

export { ClientOptions };
