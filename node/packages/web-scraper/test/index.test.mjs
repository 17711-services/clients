/**
 * Verifies every web-scraper client method sends a request to the expected path/HTTP verb and parses a well-formed response -- one test per operation, real fetch mocked via a plain reassignment of `globalThis.fetch` (no extra test/mocking dependency). Runs against the COMPILED package (`../dist/index.js`) -- build before testing.
 */

import { test } from "node:test";
import assert from "node:assert/strict";
import { Client } from "../dist/index.js";

test("extractMarkdown calls the expected path", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async (url, init = {}) => {
    const parsed = new URL(url);
    assert.equal((init.method ?? "GET").toUpperCase(), "POST");
    assert.equal(parsed.pathname, "/v1/web-scraper/extract_markdown");
    return new Response(JSON.stringify({ content_type: null, final_url: "test", markdown: "test", status: 0, title: null, truncated: false, url: "test" }), { status: 200 });
  };
  try {
    const client = new Client("https://example.test");
    const result = await client.extractMarkdown({ url: "test" });
    assert.ok(result !== undefined);
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("getTaskStatus calls the expected path", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async (url, init = {}) => {
    const parsed = new URL(url);
    assert.equal((init.method ?? "GET").toUpperCase(), "POST");
    assert.equal(parsed.pathname, "/v1/web-scraper/get_task_status");
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

test("scrapeUrl calls the expected path", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async (url, init = {}) => {
    const parsed = new URL(url);
    assert.equal((init.method ?? "GET").toUpperCase(), "POST");
    assert.equal(parsed.pathname, "/v1/web-scraper/scrape_url");
    return new Response(JSON.stringify({ content_type: null, final_url: "test", html: "test", status: 0, truncated: false, url: "test" }), { status: 200 });
  };
  try {
    const client = new Client("https://example.test");
    const result = await client.scrapeUrl({ url: "test" });
    assert.ok(result !== undefined);
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("scrapeUrlAsync calls the expected path", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async (url, init = {}) => {
    const parsed = new URL(url);
    assert.equal((init.method ?? "GET").toUpperCase(), "POST");
    assert.equal(parsed.pathname, "/v1/web-scraper/scrape_url_async");
    return new Response(JSON.stringify({ task_id: "test" }), { status: 200 });
  };
  try {
    const client = new Client("https://example.test");
    const result = await client.scrapeUrlAsync({ callback_url: null, url: "test" });
    assert.ok(result !== undefined);
  } finally {
    globalThis.fetch = originalFetch;
  }
});
