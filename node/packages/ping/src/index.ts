/**
 * Typed HTTP client and request/response interfaces for ping-service.
 */

import { Client as BaseClient, type ClientOptions } from "@xyz17711/core";

export interface PingResult {
  /** Echoes the request's own `echo` field back verbatim. */
  echo: string;
  /** This process's OS pid -- proves which process instance actually answered (useful behind a load balancer fronting several instances of the same service). */
  pid: number;
  /** Always `true` -- a client can use this as a trivial liveness/reachability check. */
  pong: boolean;
}

export interface PingRequest {
  /** Testkit-only knob (not real business logic): lets a caller simulate a slow tool call, to check whether the server dispatches concurrent calls as independent tasks rather than serializing them. */
  delay_ms?: number;
  /** Arbitrary text echoed back verbatim in the response's own `echo` field. */
  echo: string;
}

/** Production base URL of this service; pass another to self-host or test. */
export const DEFAULT_BASE_URL = "https://api.17711.xyz/registry/ping-service";

/** Typed client for ping-service, e.g. `client.ping(...)`. */
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

  /** x402 ping: the cheapest end-to-end payment test for an x402 client or agent wallet, returns an echo and the server pid ($0.002, x402) */
  async ping(request: PingRequest): Promise<PingResult> {
    return this.post<PingResult>("/v1/ping", request);
  }
}

export { ClientOptions };
