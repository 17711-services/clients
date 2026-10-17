/**
 * LangChain.js tools for 🩹 extract-correct-service, grouped in one Toolkit -- one tool per operation, each just an async function (JS has no separate sync form to generate). Requires the `@langchain/core`+`zod` peer dependencies declared in this package's own package.json -- imported from `extract-correct/langchain`, never from the package root, so importing the base client never requires them installed.
 */

import { tool } from "@langchain/core/tools";
import { z } from "zod";
import { Client } from "./index.js";

export class ExtractCorrectToolkit {
  private client: Client;

  constructor(client: Client) {
    this.client = client;
  }

  getTools() {
    return [
      tool(
        async (input) => this.client.parseJson(input),
        {
          name: "parseJson",
          description: "JSON repair API: extract valid JSON from messy text or model output and fix it against a JSON Schema ($0.006, x402)",
          schema: z.object({ schema: z.unknown().optional(), text: z.string() }),
        },
      ),
    ];
  }
}
