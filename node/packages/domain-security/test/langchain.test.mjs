/**
 * Verifies every domain-security LangChain tool through the real StructuredTool (`.invoke()`), not just the underlying client method -- catches schema-shape bugs a plain client-method test would miss. Requires the `langchain`/`zod` dev dependencies.
 */

import { test } from "node:test";
import assert from "node:assert/strict";
import { Client } from "../dist/index.js";
import { DomainSecurityToolkit } from "../dist/langchain.js";

test("getReport tool invoke", async () => {
  globalThis.fetch = async () => new Response(JSON.stringify({ age_seconds: 0, blocklisted: [], dns: { caa: [], dnssec: false, name_servers: [] }, domain: "test", findings: [], from_cache: false, grade: "test", http: { discloses_version: false, headers_missing: [], headers_present: [], http_redirects_to_https: null, https_status: null }, ip_addresses: [], mail: { dmarc: null, mta_sts: false, mx: [], provider: null, spf: null }, retrieved_at: "test", score: 0, tls: { days_remaining: null, error: null, expires_at: null, issuer: null, protocol: null, reachable: false, san_count: 0, valid: false } }), { status: 200 });
  const toolkit = new DomainSecurityToolkit(new Client("https://example.test"));
  const t = toolkit.getTools().find((x) => x.name === "getReport");
  const result = await t.invoke({ domain: "test", max_age_seconds: 0 });
  assert.ok(result !== undefined);
});
