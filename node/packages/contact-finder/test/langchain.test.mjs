/**
 * Verifies every contact-finder LangChain tool through the real StructuredTool (`.invoke()`), not just the underlying client method -- catches schema-shape bugs a plain client-method test would miss. Requires the `langchain`/`zod` dev dependencies.
 */

import { test } from "node:test";
import assert from "node:assert/strict";
import { Client } from "../dist/index.js";
import { ContactFinderToolkit } from "../dist/langchain.js";

test("getContacts tool invoke", async () => {
  globalThis.fetch = async () => new Response(JSON.stringify({ age_seconds: 0, contacts: [], domain: "test", domain_mail: { dmarc: null, mx: [], provider: null, spf: null }, from_cache: false, has_contact_form: false, omitted_non_role_addresses: 0, pages_from_cache: 0, pages_read: [], resolved_from_name: false, retrieved_at: "test", security_contact: null, source_language: "test", stale_pages: 0 }), { status: 200 });
  const toolkit = new ContactFinderToolkit(new Client("https://example.test"));
  const t = toolkit.getTools().find((x) => x.name === "getContacts");
  const result = await t.invoke({ company_name: "test", domain: "test", max_age_seconds: 0 });
  assert.ok(result !== undefined);
});
