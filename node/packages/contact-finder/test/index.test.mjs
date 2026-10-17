/**
 * Verifies every contact-finder client method sends a request to the expected path/HTTP verb and parses a well-formed response -- one test per operation, real fetch mocked via a plain reassignment of `globalThis.fetch` (no extra test/mocking dependency). Runs against the COMPILED package (`../dist/index.js`) -- build before testing.
 */

import { test } from "node:test";
import assert from "node:assert/strict";
import { Client } from "../dist/index.js";

test("getContacts calls the expected path", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async (url, init = {}) => {
    const parsed = new URL(url);
    assert.equal((init.method ?? "GET").toUpperCase(), "POST");
    assert.equal(parsed.pathname, "/v1/contact-finder/get_contacts");
    return new Response(JSON.stringify({ age_seconds: 0, contacts: [], domain: "test", domain_mail: { dmarc: null, mx: [], provider: null, spf: null }, from_cache: false, has_contact_form: false, omitted_non_role_addresses: 0, pages_from_cache: 0, pages_read: [], resolved_from_name: false, retrieved_at: "test", security_contact: null, source_language: "test", stale_pages: 0 }), { status: 200 });
  };
  try {
    const client = new Client("https://example.test");
    const result = await client.getContacts({ company_name: null, domain: null, max_age_seconds: null });
    assert.ok(result !== undefined);
  } finally {
    globalThis.fetch = originalFetch;
  }
});
