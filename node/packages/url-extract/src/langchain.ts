/**
 * LangChain.js tools for url-extract-service, grouped in one Toolkit -- one tool per operation, each just an async function (JS has no separate sync form to generate). Requires the `@langchain/core`+`zod` peer dependencies declared in this package's own package.json -- imported from `url-extract/langchain`, never from the package root, so importing the base client never requires them installed.
 */

import { tool } from "@langchain/core/tools";
import { z } from "zod";
import { Client } from "./index.js";

export class UrlExtractToolkit {
  private client: Client;

  constructor(client: Client) {
    this.client = client;
  }

  getTools() {
    return [
      tool(
        async (input) => this.client.getCompanyProfile(input),
        {
          name: "getCompanyProfile",
          description: "[Deprecated - use company_profile_get_profile] Company profile from a domain or a name as valid JSON ($0.009, x402)",
          schema: z.object({ company_name: z.string().nullable().optional(), domain: z.string().nullable().optional(), language: z.string().nullable().optional() }),
        },
      ),
      tool(
        async (input) => this.client.getStructuredData(input),
        {
          name: "getStructuredData",
          description: "URL extract with a question: ask any web page a question and get structured data as JSON that matches your schema ($0.02, x402)",
          schema: z.object({ max_age_seconds: z.number().nullable().optional(), question: z.string(), schema: z.unknown().optional(), url: z.string() }),
        },
      ),
    ];
  }
}
