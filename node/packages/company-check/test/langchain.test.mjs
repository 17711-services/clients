/**
 * Verifies every company-check LangChain tool through the real StructuredTool (`.invoke()`), not just the underlying client method -- catches schema-shape bugs a plain client-method test would miss. Requires the `langchain`/`zod` dev dependencies.
 */

import { test } from "node:test";
import assert from "node:assert/strict";
import { Client } from "../dist/index.js";
import { CompanyCheckToolkit } from "../dist/langchain.js";

test("verifyCompany tool invoke", async () => {
  globalThis.fetch = async () => new Response(JSON.stringify({ age_seconds: 0, company: { activity_code: null, address: null, closed_at: null, country: "test", created_at: null, employees: null, head_office_id: null, legal_form: null, legal_name: "test", lei: null, registration_number: null, size_category: null, status: "test", trade_name: null, vat_number: null }, confidence: "test", coverage_note: "test", directors: [], financials: [], flags: [], from_cache: false, lei: null, matched_by: "test", other_candidates: [], retrieved_at: "test", sources: [], vat: null }), { status: 200 });
  const toolkit = new CompanyCheckToolkit(new Client("https://example.test"));
  const t = toolkit.getTools().find((x) => x.name === "verifyCompany");
  const result = await t.invoke({ company_name: "test", country: "test", lei: "test", max_age_seconds: 0, registration_number: "test", vat_number: "test" });
  assert.ok(result !== undefined);
});
