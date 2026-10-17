/**
 * LangChain.js tools for 🏢 company-profile-service, grouped in one Toolkit -- one tool per operation, each just an async function (JS has no separate sync form to generate). Requires the `@langchain/core`+`zod` peer dependencies declared in this package's own package.json -- imported from `company-profile/langchain`, never from the package root, so importing the base client never requires them installed.
 */

import { tool } from "@langchain/core/tools";
import { z } from "zod";
import { Client } from "./index.js";

export class CompanyProfileToolkit {
  private client: Client;

  constructor(client: Client) {
    this.client = client;
  }

  getTools() {
    return [
      tool(
        async (input) => this.client.getProfile(input),
        {
          name: "getProfile",
          description: "Company profile and enrichment from a domain or a name: offering, public contacts, social links and WHOIS domain data as valid JSON ($0.009, x402)",
          schema: z.object({ company_name: z.string().nullable().optional(), domain: z.string().nullable().optional(), language: z.string().nullable().optional(), max_age_seconds: z.number().nullable().optional() }),
        },
      ),
    ];
  }
}
