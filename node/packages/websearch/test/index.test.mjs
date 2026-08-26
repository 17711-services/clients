/**
 * Verifies every websearch client method sends a request to the expected path/HTTP verb and parses a well-formed response -- one test per operation, real fetch mocked via a plain reassignment of `globalThis.fetch` (no extra test/mocking dependency). Runs against the COMPILED package (`../dist/index.js`) -- build before testing.
 */

import { test } from "node:test";
import assert from "node:assert/strict";
import { Client } from "../dist/index.js";

test("getTaskStatus calls the expected path", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async (url, init = {}) => {
    const parsed = new URL(url);
    assert.equal((init.method ?? "GET").toUpperCase(), "POST");
    assert.equal(parsed.pathname, "/v1/websearch/get_task_status");
    return new Response(JSON.stringify({ ok: null, result: null, status: {  } }), { status: 200 });
  };
  try {
    const client = new Client("https://example.test");
    const result = await client.getTaskStatus({ task_id: "test" });
    assert.ok(result !== undefined);
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("searchWeb calls the expected path", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async (url, init = {}) => {
    const parsed = new URL(url);
    assert.equal((init.method ?? "GET").toUpperCase(), "POST");
    assert.equal(parsed.pathname, "/v1/websearch/search_web");
    return new Response(JSON.stringify({ results: [] }), { status: 200 });
  };
  try {
    const client = new Client("https://example.test");
    const result = await client.searchWeb({ query: "test" });
    assert.ok(result !== undefined);
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("searchWebAsync calls the expected path", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async (url, init = {}) => {
    const parsed = new URL(url);
    assert.equal((init.method ?? "GET").toUpperCase(), "POST");
    assert.equal(parsed.pathname, "/v1/websearch/search_web_async");
    return new Response(JSON.stringify({ task_id: "test" }), { status: 200 });
  };
  try {
    const client = new Client("https://example.test");
    const result = await client.searchWebAsync({ callback_url: null, query: "test" });
    assert.ok(result !== undefined);
  } finally {
    globalThis.fetch = originalFetch;
  }
});
