/**
 * LangChain.js tools for 🛡️ domain-security-service, grouped in one Toolkit -- one tool per operation, each just an async function (JS has no separate sync form to generate). Requires the `@langchain/core`+`zod` peer dependencies declared in this package's own package.json -- imported from `domain-security/langchain`, never from the package root, so importing the base client never requires them installed.
 */

import { tool } from "@langchain/core/tools";
import { z } from "zod";
import { Client } from "./index.js";

export class DomainSecurityToolkit {
  private client: Client;

  constructor(client: Client) {
    this.client = client;
  }

  getTools() {
    return [
      tool(
        async (input) => this.client.getReport(input),
        {
          name: "getReport",
          description: "Domain security check: SSL certificate check, DMARC SPF check, DNSSEC, security headers and blocklist status with a score ($0.009, x402)",
          schema: z.object({ domain: z.string(), max_age_seconds: z.number().nullable().optional() }),
        },
      ),
    ];
  }
}
