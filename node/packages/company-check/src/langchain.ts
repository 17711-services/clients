/**
 * LangChain.js tools for 🏢 company-check-service, grouped in one Toolkit -- one tool per operation, each just an async function (JS has no separate sync form to generate). Requires the `@langchain/core`+`zod` peer dependencies declared in this package's own package.json -- imported from `company-check/langchain`, never from the package root, so importing the base client never requires them installed.
 */

import { tool } from "@langchain/core/tools";
import { z } from "zod";
import { Client } from "./index.js";

export class CompanyCheckToolkit {
  private client: Client;

  constructor(client: Client) {
    this.client = client;
  }

  getTools() {
    return [
      tool(
        async (input) => this.client.verifyCompany(input),
        {
          name: "verifyCompany",
          description: "Company check (KYB) and business verification: VAT validation (VIES), LEI lookup, registry status and company directors ($0.009, x402)",
          schema: z.object({ company_name: z.string().nullable().optional(), country: z.string().nullable().optional(), lei: z.string().nullable().optional(), max_age_seconds: z.number().nullable().optional(), registration_number: z.string().nullable().optional(), vat_number: z.string().nullable().optional() }),
        },
      ),
    ];
  }
}
