/**
 * Verifies every ip-blocklist client method sends a request to the expected path/HTTP verb and parses a well-formed response -- one test per operation, real fetch mocked via a plain reassignment of `globalThis.fetch` (no extra test/mocking dependency). Runs against the COMPILED package (`../dist/index.js`) -- build before testing.
 */

import { test } from "node:test";
import assert from "node:assert/strict";
import { Client } from "../dist/index.js";

test("checkIp calls the expected path", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async (url, init = {}) => {
    const parsed = new URL(url);
    assert.equal((init.method ?? "GET").toUpperCase(), "GET");
    assert.equal(parsed.pathname, "/v1/ip-blocklist/check");
    return new Response(JSON.stringify({ banned: false, ip: "test", matches: [] }), { status: 200 });
  };
  try {
    const client = new Client("https://example.test");
    const result = await client.checkIp({ ip: "test" });
    assert.ok(result !== undefined);
  } finally {
    globalThis.fetch = originalFetch;
  }
});
