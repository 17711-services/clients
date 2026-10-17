/**
 * Verifies every url-extract client method sends a request to the expected path/HTTP verb and parses a well-formed response -- one test per operation, real fetch mocked via a plain reassignment of `globalThis.fetch` (no extra test/mocking dependency). Runs against the COMPILED package (`../dist/index.js`) -- build before testing.
 */

import { test } from "node:test";
import assert from "node:assert/strict";
import { Client } from "../dist/index.js";

test("getCompanyProfile calls the expected path", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async (url, init = {}) => {
    const parsed = new URL(url);
    assert.equal((init.method ?? "GET").toUpperCase(), "POST");
    assert.equal(parsed.pathname, "/v1/url-extract/get_company_profile");
    return new Response(JSON.stringify({ applied_fixes: [], domain: "test", domain_info: { domain_age_years: null, email_provider: null, expires_at: null, mail_services: [], nameservers: [], registered_at: null, registrable_domain: "test", registrant_org: null, registrar: null, statuses: [] }, output_language: "test", pages_read: [], passes: 0, profile: null, remaining_issues: [], resolved_from_name: false, source_language: "test", unverified_removed: [], valid: null }), { status: 200 });
  };
  try {
    const client = new Client("https://example.test");
    const result = await client.getCompanyProfile({ company_name: null, domain: null, language: null });
    assert.ok(result !== undefined);
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("getStructuredData calls the expected path", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async (url, init = {}) => {
    const parsed = new URL(url);
    assert.equal((init.method ?? "GET").toUpperCase(), "POST");
    assert.equal(parsed.pathname, "/v1/url-extract/get_structured_data");
    return new Response(JSON.stringify({ age_seconds: 0, applied_fixes: [], data: null, final_url: "test", from_cache: false, page_from_cache: false, page_truncated: false, remaining_issues: [], retrieved_at: "test", stale_page: false, title: null, url: "test", valid: null }), { status: 200 });
  };
  try {
    const client = new Client("https://example.test");
    const result = await client.getStructuredData({ max_age_seconds: null, question: "test", schema: null, url: "test" });
    assert.ok(result !== undefined);
  } finally {
    globalThis.fetch = originalFetch;
  }
});
