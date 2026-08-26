/**
 * Verifies every ip-blocklist LangChain tool through the real StructuredTool (`.invoke()`), not just the underlying client method -- catches schema-shape bugs a plain client-method test would miss. Requires the `langchain`/`zod` dev dependencies.
 */

import { test } from "node:test";
import assert from "node:assert/strict";
import { Client } from "../dist/index.js";
import { IpBlocklistToolkit } from "../dist/langchain.js";

test("checkIp tool invoke", async () => {
  globalThis.fetch = async () => new Response(JSON.stringify({ banned: false, ip: "test", matches: [] }), { status: 200 });
  const toolkit = new IpBlocklistToolkit(new Client("https://example.test"));
  const t = toolkit.getTools().find((x) => x.name === "checkIp");
  const result = await t.invoke({ ip: "test" });
  assert.ok(result !== undefined);
});
