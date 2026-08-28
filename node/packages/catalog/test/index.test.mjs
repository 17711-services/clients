/**
 * Verifies every catalog client method sends a request to the expected path/HTTP verb and parses a well-formed response -- one test per operation, real fetch mocked via a plain reassignment of `globalThis.fetch` (no extra test/mocking dependency). Runs against the COMPILED package (`../dist/index.js`) -- build before testing.
 */

import { test } from "node:test";
import assert from "node:assert/strict";
import { Client } from "../dist/index.js";

test("category calls the expected path", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async (url, init = {}) => {
    const parsed = new URL(url);
    assert.equal((init.method ?? "GET").toUpperCase(), "GET");
    assert.equal(parsed.pathname, "/v1/catalog/category");
    return new Response(JSON.stringify({ entries: [], limit: 0, offset: 0, total_count: 0 }), { status: 200 });
  };
  try {
    const client = new Client("https://example.test");
    const result = await client.category({ q: "test", limit: null, offset: null });
    assert.ok(result !== undefined);
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("findServicesByCapability calls the expected path", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async (url, init = {}) => {
    const parsed = new URL(url);
    assert.equal((init.method ?? "GET").toUpperCase(), "POST");
    assert.equal(parsed.pathname, "/v1/catalog/find_services_by_capability");
    return new Response(JSON.stringify({ results: [] }), { status: 200 });
  };
  try {
    const client = new Client("https://example.test");
    const result = await client.findServicesByCapability({ query: "test", top_k: null });
    assert.ok(result !== undefined);
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("search calls the expected path", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async (url, init = {}) => {
    const parsed = new URL(url);
    assert.equal((init.method ?? "GET").toUpperCase(), "GET");
    assert.equal(parsed.pathname, "/v1/catalog/search");
    return new Response(JSON.stringify({ results: [] }), { status: 200 });
  };
  try {
    const client = new Client("https://example.test");
    const result = await client.search({ q: "test", category: null, limit: null });
    assert.ok(result !== undefined);
  } finally {
    globalThis.fetch = originalFetch;
  }
});
