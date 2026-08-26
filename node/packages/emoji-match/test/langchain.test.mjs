/**
 * Verifies every emoji-match LangChain tool through the real StructuredTool (`.invoke()`), not just the underlying client method -- catches schema-shape bugs a plain client-method test would miss. Requires the `langchain`/`zod` dev dependencies.
 */

import { test } from "node:test";
import assert from "node:assert/strict";
import { Client } from "../dist/index.js";
import { EmojiMatchToolkit } from "../dist/langchain.js";

test("suggestEmojis tool invoke", async () => {
  globalThis.fetch = async () => new Response(JSON.stringify({ emojis: [], matched_language: "test" }), { status: 200 });
  const toolkit = new EmojiMatchToolkit(new Client("https://example.test"));
  const t = toolkit.getTools().find((x) => x.name === "suggestEmojis");
  const result = await t.invoke({ text: "test" });
  assert.ok(result !== undefined);
});
