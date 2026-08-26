/**
 * Verifies every ping LangChain tool through the real StructuredTool (`.invoke()`), not just the underlying client method -- catches schema-shape bugs a plain client-method test would miss. Requires the `langchain`/`zod` dev dependencies.
 */

import { test } from "node:test";
import assert from "node:assert/strict";
import { Client } from "../dist/index.js";
import { PingToolkit } from "../dist/langchain.js";

test("ping tool invoke", async () => {
  globalThis.fetch = async () => new Response(JSON.stringify({ echo: "test", pid: 0, pong: false }), { status: 200 });
  const toolkit = new PingToolkit(new Client("https://example.test"));
  const t = toolkit.getTools().find((x) => x.name === "ping");
  const result = await t.invoke({ delay_ms: 0, echo: "test" });
  assert.ok(result !== undefined);
});
