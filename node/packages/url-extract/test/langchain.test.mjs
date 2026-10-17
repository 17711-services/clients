/**
 * Verifies every url-extract LangChain tool through the real StructuredTool (`.invoke()`), not just the underlying client method -- catches schema-shape bugs a plain client-method test would miss. Requires the `langchain`/`zod` dev dependencies.
 */

import { test } from "node:test";
import assert from "node:assert/strict";
import { Client } from "../dist/index.js";
import { UrlExtractToolkit } from "../dist/langchain.js";

test("getCompanyProfile tool invoke", async () => {
  globalThis.fetch = async () => new Response(JSON.stringify({ applied_fixes: [], domain: "test", domain_info: { domain_age_years: null, email_provider: null, expires_at: null, mail_services: [], nameservers: [], registered_at: null, registrable_domain: "test", registrant_org: null, registrar: null, statuses: [] }, output_language: "test", pages_read: [], passes: 0, profile: null, remaining_issues: [], resolved_from_name: false, source_language: "test", unverified_removed: [], valid: null }), { status: 200 });
  const toolkit = new UrlExtractToolkit(new Client("https://example.test"));
  const t = toolkit.getTools().find((x) => x.name === "getCompanyProfile");
  const result = await t.invoke({ company_name: "test", domain: "test", language: "test" });
  assert.ok(result !== undefined);
});

test("getStructuredData tool invoke", async () => {
  globalThis.fetch = async () => new Response(JSON.stringify({ age_seconds: 0, applied_fixes: [], data: null, final_url: "test", from_cache: false, page_from_cache: false, page_truncated: false, remaining_issues: [], retrieved_at: "test", stale_page: false, title: null, url: "test", valid: null }), { status: 200 });
  const toolkit = new UrlExtractToolkit(new Client("https://example.test"));
  const t = toolkit.getTools().find((x) => x.name === "getStructuredData");
  const result = await t.invoke({ max_age_seconds: 0, question: "test", schema: null, url: "test" });
  assert.ok(result !== undefined);
});
