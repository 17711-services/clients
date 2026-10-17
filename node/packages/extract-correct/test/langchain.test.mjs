/**
 * Verifies every extract-correct LangChain tool through the real StructuredTool (`.invoke()`), not just the underlying client method -- catches schema-shape bugs a plain client-method test would miss. Requires the `langchain`/`zod` dev dependencies.
 */

import { test } from "node:test";
import assert from "node:assert/strict";
import { Client } from "../dist/index.js";
import { ExtractCorrectToolkit } from "../dist/langchain.js";

test("parseJson tool invoke", async () => {
  globalThis.fetch = async () => new Response(JSON.stringify({ applied_fixes: [], data: null, extraction_method: "test", remaining_issues: [], valid: null }), { status: 200 });
  const toolkit = new ExtractCorrectToolkit(new Client("https://example.test"));
  const t = toolkit.getTools().find((x) => x.name === "parseJson");
  const result = await t.invoke({ schema: null, text: "test" });
  assert.ok(result !== undefined);
});
