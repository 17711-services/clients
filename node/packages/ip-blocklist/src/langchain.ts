/**
 * LangChain.js tools for ip-blocklist, grouped in one Toolkit -- one tool per operation, each just an async function (JS has no separate sync form to generate). Requires the `@langchain/core`+`zod` peer dependencies declared in this package's own package.json -- imported from `ip-blocklist/langchain`, never from the package root, so importing the base client never requires them installed.
 */

import { tool } from "@langchain/core/tools";
import { z } from "zod";
import { Client } from "./index.js";

export class IpBlocklistToolkit {
  private client: Client;

  constructor(client: Client) {
    this.client = client;
  }

  getTools() {
    return [
      tool(
        async (input) => this.client.checkIp(input),
        {
          name: "checkIp",
          description: "Checks whether an IPv4 address appears on any of several public IP blocklists ($0.002, x402)",
          schema: z.object({ ip: z.string() }),
        },
      ),
    ];
  }
}
