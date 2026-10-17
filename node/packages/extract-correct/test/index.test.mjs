/**
 * Verifies every extract-correct client method sends a request to the expected path/HTTP verb and parses a well-formed response -- one test per operation, real fetch mocked via a plain reassignment of `globalThis.fetch` (no extra test/mocking dependency). Runs against the COMPILED package (`../dist/index.js`) -- build before testing.
 */

import { test } from "node:test";
import assert from "node:assert/strict";
import { Client } from "../dist/index.js";

test("parseJson calls the expected path", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async (url, init = {}) => {
    const parsed = new URL(url);
    assert.equal((init.method ?? "GET").toUpperCase(), "POST");
    assert.equal(parsed.pathname, "/v1/extract-correct/parse_json");
    return new Response(JSON.stringify({ applied_fixes: [], data: null, extraction_method: "test", remaining_issues: [], valid: null }), { status: 200 });
  };
  try {
    const client = new Client("https://example.test");
    const result = await client.parseJson({ schema: null, text: "test" });
    assert.ok(result !== undefined);
  } finally {
    globalThis.fetch = originalFetch;
  }
});
