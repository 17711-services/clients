/**
 * Verifies every catalog LangChain tool through the real StructuredTool (`.invoke()`), not just the underlying client method -- catches schema-shape bugs a plain client-method test would miss. Requires the `langchain`/`zod` dev dependencies.
 */

import { test } from "node:test";
import assert from "node:assert/strict";
import { Client } from "../dist/index.js";
import { CatalogToolkit } from "../dist/langchain.js";

test("category tool invoke", async () => {
  globalThis.fetch = async () => new Response(JSON.stringify({ entries: [], limit: 0, offset: 0, total_count: 0 }), { status: 200 });
  const toolkit = new CatalogToolkit(new Client("https://example.test"));
  const t = toolkit.getTools().find((x) => x.name === "category");
  const result = await t.invoke({ q: "test", limit: 0, offset: 0 });
  assert.ok(result !== undefined);
});

test("findServicesByCapability tool invoke", async () => {
  globalThis.fetch = async () => new Response(JSON.stringify({ results: [] }), { status: 200 });
  const toolkit = new CatalogToolkit(new Client("https://example.test"));
  const t = toolkit.getTools().find((x) => x.name === "findServicesByCapability");
  const result = await t.invoke({ query: "test", top_k: 0 });
  assert.ok(result !== undefined);
});

test("search tool invoke", async () => {
  globalThis.fetch = async () => new Response(JSON.stringify({ results: [] }), { status: 200 });
  const toolkit = new CatalogToolkit(new Client("https://example.test"));
  const t = toolkit.getTools().find((x) => x.name === "search");
  const result = await t.invoke({ q: "test", category: "test", limit: 0 });
  assert.ok(result !== undefined);
});
