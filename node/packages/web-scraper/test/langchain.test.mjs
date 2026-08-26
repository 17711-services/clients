/**
 * Verifies every web-scraper LangChain tool through the real StructuredTool (`.invoke()`), not just the underlying client method -- catches schema-shape bugs a plain client-method test would miss. Requires the `langchain`/`zod` dev dependencies.
 */

import { test } from "node:test";
import assert from "node:assert/strict";
import { Client } from "../dist/index.js";
import { WebScraperToolkit } from "../dist/langchain.js";

test("extractMarkdown tool invoke", async () => {
  globalThis.fetch = async () => new Response(JSON.stringify({ content_type: null, final_url: "test", markdown: "test", status: 0, title: null, truncated: false, url: "test" }), { status: 200 });
  const toolkit = new WebScraperToolkit(new Client("https://example.test"));
  const t = toolkit.getTools().find((x) => x.name === "extractMarkdown");
  const result = await t.invoke({ url: "test" });
  assert.ok(result !== undefined);
});

test("getTaskStatus tool invoke", async () => {
  globalThis.fetch = async () => new Response(JSON.stringify({ ok: null, result: null, status: {  } }), { status: 200 });
  const toolkit = new WebScraperToolkit(new Client("https://example.test"));
  const t = toolkit.getTools().find((x) => x.name === "getTaskStatus");
  const result = await t.invoke({ task_id: "test" });
  assert.ok(result !== undefined);
});

test("scrapeUrl tool invoke", async () => {
  globalThis.fetch = async () => new Response(JSON.stringify({ content_type: null, final_url: "test", html: "test", status: 0, truncated: false, url: "test" }), { status: 200 });
  const toolkit = new WebScraperToolkit(new Client("https://example.test"));
  const t = toolkit.getTools().find((x) => x.name === "scrapeUrl");
  const result = await t.invoke({ url: "test" });
  assert.ok(result !== undefined);
});

test("scrapeUrlAsync tool invoke", async () => {
  globalThis.fetch = async () => new Response(JSON.stringify({ task_id: "test" }), { status: 200 });
  const toolkit = new WebScraperToolkit(new Client("https://example.test"));
  const t = toolkit.getTools().find((x) => x.name === "scrapeUrlAsync");
  const result = await t.invoke({ callback_url: "test", url: "test" });
  assert.ok(result !== undefined);
});
