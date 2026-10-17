/**
 * LangChain.js tools for sanctions-check-service, grouped in one Toolkit -- one tool per operation, each just an async function (JS has no separate sync form to generate). Requires the `@langchain/core`+`zod` peer dependencies declared in this package's own package.json -- imported from `sanctions-check/langchain`, never from the package root, so importing the base client never requires them installed.
 */

import { tool } from "@langchain/core/tools";
import { z } from "zod";
import { Client } from "./index.js";

export class SanctionsCheckToolkit {
  private client: Client;

  constructor(client: Client) {
    this.client = client;
  }

  getTools() {
    return [
      tool(
        async (input) => this.client.screenName(input),
        {
          name: "screenName",
          description: "Sanctions check: OFAC list check and sanctions screening of a person or company name against OFAC SDN, EU and UN lists (AML KYC) ($0.01, x402)",
          schema: z.object({ birth_year: z.number().nullable().optional(), name: z.string(), type: z.string().nullable().optional() }),
        },
      ),
    ];
  }
}
