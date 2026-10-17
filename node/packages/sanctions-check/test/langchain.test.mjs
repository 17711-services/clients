/**
 * Verifies every sanctions-check LangChain tool through the real StructuredTool (`.invoke()`), not just the underlying client method -- catches schema-shape bugs a plain client-method test would miss. Requires the `langchain`/`zod` dev dependencies.
 */

import { test } from "node:test";
import assert from "node:assert/strict";
import { Client } from "../dist/index.js";
import { SanctionsCheckToolkit } from "../dist/langchain.js";

test("screenName tool invoke", async () => {
  globalThis.fetch = async () => new Response(JSON.stringify({ disclaimer: "test", lists_missing: [], lists_screened: [], matches: [], name: "test", screened_at: "test", verdict: "test" }), { status: 200 });
  const toolkit = new SanctionsCheckToolkit(new Client("https://example.test"));
  const t = toolkit.getTools().find((x) => x.name === "screenName");
  const result = await t.invoke({ birth_year: 0, name: "test", type: "test" });
  assert.ok(result !== undefined);
});
