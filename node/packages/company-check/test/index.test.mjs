/**
 * Verifies every company-check client method sends a request to the expected path/HTTP verb and parses a well-formed response -- one test per operation, real fetch mocked via a plain reassignment of `globalThis.fetch` (no extra test/mocking dependency). Runs against the COMPILED package (`../dist/index.js`) -- build before testing.
 */

import { test } from "node:test";
import assert from "node:assert/strict";
import { Client } from "../dist/index.js";

test("verifyCompany calls the expected path", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async (url, init = {}) => {
    const parsed = new URL(url);
    assert.equal((init.method ?? "GET").toUpperCase(), "POST");
    assert.equal(parsed.pathname, "/v1/company-check/verify_company");
    return new Response(JSON.stringify({ age_seconds: 0, company: { activity_code: null, address: null, closed_at: null, country: "test", created_at: null, employees: null, head_office_id: null, legal_form: null, legal_name: "test", lei: null, registration_number: null, size_category: null, status: "test", trade_name: null, vat_number: null }, confidence: "test", coverage_note: "test", directors: [], financials: [], flags: [], from_cache: false, lei: null, matched_by: "test", other_candidates: [], retrieved_at: "test", sources: [], vat: null }), { status: 200 });
  };
  try {
    const client = new Client("https://example.test");
    const result = await client.verifyCompany({ company_name: null, country: null, lei: null, max_age_seconds: null, registration_number: null, vat_number: null });
    assert.ok(result !== undefined);
  } finally {
    globalThis.fetch = originalFetch;
  }
});
