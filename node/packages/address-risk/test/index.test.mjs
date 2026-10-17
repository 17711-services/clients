/**
 * Verifies every address-risk client method sends a request to the expected path/HTTP verb and parses a well-formed response -- one test per operation, real fetch mocked via a plain reassignment of `globalThis.fetch` (no extra test/mocking dependency). Runs against the COMPILED package (`../dist/index.js`) -- build before testing.
 */

import { test } from "node:test";
import assert from "node:assert/strict";
import { Client } from "../dist/index.js";

test("checkAddress calls the expected path", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async (url, init = {}) => {
    const parsed = new URL(url);
    assert.equal((init.method ?? "GET").toUpperCase(), "POST");
    assert.equal(parsed.pathname, "/v1/address-risk/check_address");
    return new Response(JSON.stringify({ address: "test", age_seconds: 0, chain: "test", disclaimer: "test", flags: [], from_cache: false, kind: "test", reported_by: null, retrieved_at: "test", safety_score: 0, verdict: "test" }), { status: 200 });
  };
  try {
    const client = new Client("https://example.test");
    const result = await client.checkAddress({ address: "test", chain: null, max_age_seconds: null });
    assert.ok(result !== undefined);
  } finally {
    globalThis.fetch = originalFetch;
  }
});
