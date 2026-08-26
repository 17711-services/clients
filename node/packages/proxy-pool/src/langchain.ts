/**
 * LangChain.js tools for proxy-pool, grouped in one Toolkit -- one tool per operation, each just an async function (JS has no separate sync form to generate). Requires the `@langchain/core`+`zod` peer dependencies declared in this package's own package.json -- imported from `proxy-pool/langchain`, never from the package root, so importing the base client never requires them installed.
 */

import { tool } from "@langchain/core/tools";
import { z } from "zod";
import { Client } from "./index.js";

export class ProxyPoolToolkit {
  private client: Client;

  constructor(client: Client) {
    this.client = client;
  }

  getTools() {
    return [
      tool(
        async (input) => this.client.getBestProxy(input),
        {
          name: "getBestProxy",
          description: "Returns one of the fastest verified-alive proxies matching the filter, randomized to spread load ($0.001, x402)",
          schema: z.object({ anonymity: z.string().nullable().optional(), city: z.string().nullable().optional(), country: z.string().nullable().optional(), protocol: z.string().nullable().optional() }),
        },
      ),
    ];
  }
}
