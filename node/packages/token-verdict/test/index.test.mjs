/**
 * Verifies every token-verdict client method sends a request to the expected path/HTTP verb and parses a well-formed response -- one test per operation, real fetch mocked via a plain reassignment of `globalThis.fetch` (no extra test/mocking dependency). Runs against the COMPILED package (`../dist/index.js`) -- build before testing.
 */

import { test } from "node:test";
import assert from "node:assert/strict";
import { Client } from "../dist/index.js";

test("getVerdict calls the expected path", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async (url, init = {}) => {
    const parsed = new URL(url);
    assert.equal((init.method ?? "GET").toUpperCase(), "POST");
    assert.equal(parsed.pathname, "/v1/token-verdict/get_verdict");
    return new Response(JSON.stringify({ address: "test", age_seconds: 0, chain: "test", contract: { blacklist: null, hidden_owner: null, mintable: null, owner: null, owner_can_reclaim: null, ownership_renounced: false, pausable: null, proxy: null, self_destruct: null, source_verified: null, taxes_modifiable: null }, disclaimer: "test", findings: [], from_cache: false, holders: { count: null, creator_percent: null, owner_percent: null, top10_wallets_percent: null }, liquidity: { locked_percent: null, pool_age_days: null, pools: 0, top_pool: null, total_usd: 0 }, market: { buys_24h: 0, fully_diluted_value_usd: null, price_change_24h_percent: null, price_usd: null, sells_24h: 0, volume_24h_usd: 0 }, name: null, retrieved_at: "test", safety_score: 0, sources: [], symbol: null, trading: { buy_tax_percent: null, cannot_sell_all: null, honeypot: null, sell_tax_percent: null }, verdict: "test" }), { status: 200 });
  };
  try {
    const client = new Client("https://example.test");
    const result = await client.getVerdict({ address: "test", chain: null, max_age_seconds: null });
    assert.ok(result !== undefined);
  } finally {
    globalThis.fetch = originalFetch;
  }
});
