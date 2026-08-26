/**
 * LangChain.js tools for emoji-match-service, grouped in one Toolkit -- one tool per operation, each just an async function (JS has no separate sync form to generate). Requires the `@langchain/core`+`zod` peer dependencies declared in this package's own package.json -- imported from `emoji-match/langchain`, never from the package root, so importing the base client never requires them installed.
 */

import { tool } from "@langchain/core/tools";
import { z } from "zod";
import { Client } from "./index.js";

export class EmojiMatchToolkit {
  private client: Client;

  constructor(client: Client) {
    this.client = client;
  }

  getTools() {
    return [
      tool(
        async (input) => this.client.suggestEmojis(input),
        {
          name: "suggestEmojis",
          description: "Suggests 1-5 emoji matching a text's lexicon, English/French best-supported ($0.001, x402)",
          schema: z.object({ text: z.string() }),
        },
      ),
    ];
  }
}
