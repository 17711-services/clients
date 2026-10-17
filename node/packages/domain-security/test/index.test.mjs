/**
 * Verifies every domain-security client method sends a request to the expected path/HTTP verb and parses a well-formed response -- one test per operation, real fetch mocked via a plain reassignment of `globalThis.fetch` (no extra test/mocking dependency). Runs against the COMPILED package (`../dist/index.js`) -- build before testing.
 */

import { test } from "node:test";
import assert from "node:assert/strict";
import { Client } from "../dist/index.js";

test("getReport calls the expected path", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async (url, init = {}) => {
    const parsed = new URL(url);
    assert.equal((init.method ?? "GET").toUpperCase(), "POST");
    assert.equal(parsed.pathname, "/v1/domain-security/get_report");
    return new Response(JSON.stringify({ age_seconds: 0, blocklisted: [], dns: { caa: [], dnssec: false, name_servers: [] }, domain: "test", findings: [], from_cache: false, grade: "test", http: { discloses_version: false, headers_missing: [], headers_present: [], http_redirects_to_https: null, https_status: null }, ip_addresses: [], mail: { dmarc: null, mta_sts: false, mx: [], provider: null, spf: null }, retrieved_at: "test", score: 0, tls: { days_remaining: null, error: null, expires_at: null, issuer: null, protocol: null, reachable: false, san_count: 0, valid: false } }), { status: 200 });
  };
  try {
    const client = new Client("https://example.test");
    const result = await client.getReport({ domain: "test", max_age_seconds: null });
    assert.ok(result !== undefined);
  } finally {
    globalThis.fetch = originalFetch;
  }
});
