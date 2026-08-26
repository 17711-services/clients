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

/** Typed client for proxy-pool, e.g. `client.getBestProxy(...)`. */
export class Client extends BaseClient {
  /** Returns one of the fastest verified-alive proxies matching the filter, randomized to spread load ($0.001, x402) */
  async getBestProxy(params: { anonymity?: string | null; city?: string | null; country?: string | null; protocol?: string | null }): Promise<GetBestProxyResponse> {
    return this.get<GetBestProxyResponse>("/v1/proxy-pool/get_best_proxy", { anonymity: params.anonymity, city: params.city, country: params.country, protocol: params.protocol });
  }
}

export { ClientOptions };
