/**
 * LangChain.js tools for ping-service, grouped in one Toolkit -- one tool per operation, each just an async function (JS has no separate sync form to generate). Requires the `@langchain/core`+`zod` peer dependencies declared in this package's own package.json -- imported from `ping/langchain`, never from the package root, so importing the base client never requires them installed.
 */

import { tool } from "@langchain/core/tools";
import { z } from "zod";
import { Client } from "./index.js";

export class PingToolkit {
  private client: Client;

  constructor(client: Client) {
    this.client = client;
  }

  getTools() {
    return [
      tool(
        async (input) => this.client.ping(input),
        {
          name: "ping",
          description: "Echoes back the input plus this process's pid ($0.001, x402)",
          schema: z.object({ delay_ms: z.number().optional(), echo: z.string() }),
        },
      ),
    ];
  }
}
