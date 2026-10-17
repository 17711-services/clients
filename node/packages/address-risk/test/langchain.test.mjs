/**
 * Verifies every address-risk LangChain tool through the real StructuredTool (`.invoke()`), not just the underlying client method -- catches schema-shape bugs a plain client-method test would miss. Requires the `langchain`/`zod` dev dependencies.
 */

import { test } from "node:test";
import assert from "node:assert/strict";
import { Client } from "../dist/index.js";
import { AddressRiskToolkit } from "../dist/langchain.js";

test("checkAddress tool invoke", async () => {
  globalThis.fetch = async () => new Response(JSON.stringify({ address: "test", age_seconds: 0, chain: "test", disclaimer: "test", flags: [], from_cache: false, kind: "test", reported_by: null, retrieved_at: "test", safety_score: 0, verdict: "test" }), { status: 200 });
  const toolkit = new AddressRiskToolkit(new Client("https://example.test"));
  const t = toolkit.getTools().find((x) => x.name === "checkAddress");
  const result = await t.invoke({ address: "test", chain: "test", max_age_seconds: 0 });
  assert.ok(result !== undefined);
});
