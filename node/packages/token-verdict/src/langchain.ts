/**
 * LangChain.js tools for 🪙 token-verdict-service, grouped in one Toolkit -- one tool per operation, each just an async function (JS has no separate sync form to generate). Requires the `@langchain/core`+`zod` peer dependencies declared in this package's own package.json -- imported from `token-verdict/langchain`, never from the package root, so importing the base client never requires them installed.
 */

import { tool } from "@langchain/core/tools";
import { z } from "zod";
import { Client } from "./index.js";

export class TokenVerdictToolkit {
  private client: Client;

  constructor(client: Client) {
    this.client = client;
  }

  getTools() {
    return [
      tool(
        async (input) => this.client.getVerdict(input),
        {
          name: "getVerdict",
          description: "Token verdict and security check: is this token safe? Honeypot, rug pull and scam detection with taxes, liquidity and admin powers ($0.01, x402)",
          schema: z.object({ address: z.string(), chain: z.string().nullable().optional(), max_age_seconds: z.number().nullable().optional() }),
        },
      ),
    ];
  }
}
