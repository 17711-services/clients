/**
 * Verifies every proxy-pool LangChain tool through the real StructuredTool (`.invoke()`), not just the underlying client method -- catches schema-shape bugs a plain client-method test would miss. Requires the `langchain`/`zod` dev dependencies.
 */

import { test } from "node:test";
import assert from "node:assert/strict";
import { Client } from "../dist/index.js";
import { ProxyPoolToolkit } from "../dist/langchain.js";

test("getBestProxy tool invoke", async () => {
  globalThis.fetch = async () => new Response(JSON.stringify({ proxy: { anonymity: "test", checked_alive: null, checked_at: null, checked_consecutive_successes: 0, checked_ema_latency_ms: null, checked_latency_ms: null, checked_protocol: null, city: "test", country: "test", id: "test", ip: "test", port: 0, protocols: [] } }), { status: 200 });
  const toolkit = new ProxyPoolToolkit(new Client("https://example.test"));
  const t = toolkit.getTools().find((x) => x.name === "getBestProxy");
  const result = await t.invoke({ anonymity: "test", city: "test", country: "test", protocol: "test" });
  assert.ok(result !== undefined);
});
