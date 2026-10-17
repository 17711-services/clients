/**
 * Verifies every token-verdict LangChain tool through the real StructuredTool (`.invoke()`), not just the underlying client method -- catches schema-shape bugs a plain client-method test would miss. Requires the `langchain`/`zod` dev dependencies.
 */

import { test } from "node:test";
import assert from "node:assert/strict";
import { Client } from "../dist/index.js";
import { TokenVerdictToolkit } from "../dist/langchain.js";

test("getVerdict tool invoke", async () => {
  globalThis.fetch = async () => new Response(JSON.stringify({ address: "test", age_seconds: 0, chain: "test", contract: { blacklist: null, hidden_owner: null, mintable: null, owner: null, owner_can_reclaim: null, ownership_renounced: false, pausable: null, proxy: null, self_destruct: null, source_verified: null, taxes_modifiable: null }, disclaimer: "test", findings: [], from_cache: false, holders: { count: null, creator_percent: null, owner_percent: null, top10_wallets_percent: null }, liquidity: { locked_percent: null, pool_age_days: null, pools: 0, top_pool: null, total_usd: 0 }, market: { buys_24h: 0, fully_diluted_value_usd: null, price_change_24h_percent: null, price_usd: null, sells_24h: 0, volume_24h_usd: 0 }, name: null, retrieved_at: "test", safety_score: 0, sources: [], symbol: null, trading: { buy_tax_percent: null, cannot_sell_all: null, honeypot: null, sell_tax_percent: null }, verdict: "test" }), { status: 200 });
  const toolkit = new TokenVerdictToolkit(new Client("https://example.test"));
  const t = toolkit.getTools().find((x) => x.name === "getVerdict");
  const result = await t.invoke({ address: "test", chain: "test", max_age_seconds: 0 });
  assert.ok(result !== undefined);
});
