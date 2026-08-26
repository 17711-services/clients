/**
 * Verifies every proxy-pool client method sends a request to the expected path/HTTP verb and parses a well-formed response -- one test per operation, real fetch mocked via a plain reassignment of `globalThis.fetch` (no extra test/mocking dependency). Runs against the COMPILED package (`../dist/index.js`) -- build before testing.
 */

import { test } from "node:test";
import assert from "node:assert/strict";
import { Client } from "../dist/index.js";

test("getBestProxy calls the expected path", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async (url, init = {}) => {
    const parsed = new URL(url);
    assert.equal((init.method ?? "GET").toUpperCase(), "GET");
    assert.equal(parsed.pathname, "/v1/proxy-pool/get_best_proxy");
    return new Response(JSON.stringify({ proxy: { anonymity: "test", checked_alive: null, checked_at: null, checked_consecutive_successes: 0, checked_ema_latency_ms: null, checked_latency_ms: null, checked_protocol: null, city: "test", country: "test", id: "test", ip: "test", port: 0, protocols: [] } }), { status: 200 });
  };
  try {
    const client = new Client("https://example.test");
    const result = await client.getBestProxy({ anonymity: null, city: null, country: null, protocol: null });
    assert.ok(result !== undefined);
  } finally {
    globalThis.fetch = originalFetch;
  }
});
