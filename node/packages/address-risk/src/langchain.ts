/**
 * LangChain.js tools for address-risk-service, grouped in one Toolkit -- one tool per operation, each just an async function (JS has no separate sync form to generate). Requires the `@langchain/core`+`zod` peer dependencies declared in this package's own package.json -- imported from `address-risk/langchain`, never from the package root, so importing the base client never requires them installed.
 */

import { tool } from "@langchain/core/tools";
import { z } from "zod";
import { Client } from "./index.js";

export class AddressRiskToolkit {
  private client: Client;

  constructor(client: Client) {
    this.client = client;
  }

  getTools() {
    return [
      tool(
        async (input) => this.client.checkAddress(input),
        {
          name: "checkAddress",
          description: "Wallet address risk check: sanctioned address and phishing check for a crypto wallet or contract before you send funds, with theft, scam, mixer and blacklist flags ($0.005, x402)",
          schema: z.object({ address: z.string(), chain: z.string().nullable().optional(), max_age_seconds: z.number().nullable().optional() }),
        },
      ),
    ];
  }
}
