/**
 * Verifies every company-profile client method sends a request to the expected path/HTTP verb and parses a well-formed response -- one test per operation, real fetch mocked via a plain reassignment of `globalThis.fetch` (no extra test/mocking dependency). Runs against the COMPILED package (`../dist/index.js`) -- build before testing.
 */

import { test } from "node:test";
import assert from "node:assert/strict";
import { Client } from "../dist/index.js";

test("getProfile calls the expected path", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async (url, init = {}) => {
    const parsed = new URL(url);
    assert.equal((init.method ?? "GET").toUpperCase(), "POST");
    assert.equal(parsed.pathname, "/v1/company-profile/get_profile");
    return new Response(JSON.stringify({ age_seconds: 0, applied_fixes: [], domain: "test", domain_info: { domain_age_years: null, email_provider: null, expires_at: null, mail_services: [], nameservers: [], registered_at: null, registrable_domain: "test", registrant_org: null, registrar: null, statuses: [] }, from_cache: false, output_language: "test", pages_from_cache: 0, pages_read: [], passes: 0, profile: null, remaining_issues: [], resolved_from_name: false, retrieved_at: "test", source_language: "test", stale_pages: 0, unverified_removed: [], valid: null }), { status: 200 });
  };
  try {
    const client = new Client("https://example.test");
    const result = await client.getProfile({ company_name: null, domain: null, language: null, max_age_seconds: null });
    assert.ok(result !== undefined);
  } finally {
    globalThis.fetch = originalFetch;
  }
});
