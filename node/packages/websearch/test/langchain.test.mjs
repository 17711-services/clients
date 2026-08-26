/**
 * Verifies every websearch LangChain tool through the real StructuredTool (`.invoke()`), not just the underlying client method -- catches schema-shape bugs a plain client-method test would miss. Requires the `langchain`/`zod` dev dependencies.
 */

import { test } from "node:test";
import assert from "node:assert/strict";
import { Client } from "../dist/index.js";
import { WebsearchToolkit } from "../dist/langchain.js";

test("getTaskStatus tool invoke", async () => {
  globalThis.fetch = async () => new Response(JSON.stringify({ ok: null, result: null, status: {  } }), { status: 200 });
  const toolkit = new WebsearchToolkit(new Client("https://example.test"));
  const t = toolkit.getTools().find((x) => x.name === "getTaskStatus");
  const result = await t.invoke({ task_id: "test" });
  assert.ok(result !== undefined);
});

test("searchWeb tool invoke", async () => {
  globalThis.fetch = async () => new Response(JSON.stringify({ results: [] }), { status: 200 });
  const toolkit = new WebsearchToolkit(new Client("https://example.test"));
  const t = toolkit.getTools().find((x) => x.name === "searchWeb");
  const result = await t.invoke({ query: "test" });
  assert.ok(result !== undefined);
});

test("searchWebAsync tool invoke", async () => {
  globalThis.fetch = async () => new Response(JSON.stringify({ task_id: "test" }), { status: 200 });
  const toolkit = new WebsearchToolkit(new Client("https://example.test"));
  const t = toolkit.getTools().find((x) => x.name === "searchWebAsync");
  const result = await t.invoke({ callback_url: "test", query: "test" });
  assert.ok(result !== undefined);
});
