/**
 * Verifies every company-profile LangChain tool through the real StructuredTool (`.invoke()`), not just the underlying client method -- catches schema-shape bugs a plain client-method test would miss. Requires the `langchain`/`zod` dev dependencies.
 */

import { test } from "node:test";
import assert from "node:assert/strict";
import { Client } from "../dist/index.js";
import { CompanyProfileToolkit } from "../dist/langchain.js";

test("getProfile tool invoke", async () => {
  globalThis.fetch = async () => new Response(JSON.stringify({ age_seconds: 0, applied_fixes: [], domain: "test", domain_info: { domain_age_years: null, email_provider: null, expires_at: null, mail_services: [], nameservers: [], registered_at: null, registrable_domain: "test", registrant_org: null, registrar: null, statuses: [] }, from_cache: false, output_language: "test", pages_from_cache: 0, pages_read: [], passes: 0, profile: null, remaining_issues: [], resolved_from_name: false, retrieved_at: "test", source_language: "test", stale_pages: 0, unverified_removed: [], valid: null }), { status: 200 });
  const toolkit = new CompanyProfileToolkit(new Client("https://example.test"));
  const t = toolkit.getTools().find((x) => x.name === "getProfile");
  const result = await t.invoke({ company_name: "test", domain: "test", language: "test", max_age_seconds: 0 });
  assert.ok(result !== undefined);
});
