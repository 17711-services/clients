/**
 * LangChain.js tools for catalog, grouped in one Toolkit -- one tool per operation, each just an async function (JS has no separate sync form to generate). Requires the `@langchain/core`+`zod` peer dependencies declared in this package's own package.json -- imported from `catalog/langchain`, never from the package root, so importing the base client never requires them installed.
 */

import { tool } from "@langchain/core/tools";
import { z } from "zod";
import { Client } from "./index.js";

export class CatalogToolkit {
  private client: Client;

  constructor(client: Client) {
    this.client = client;
  }

  getTools() {
    return [
      tool(
        async (input) => this.client.category(input),
        {
          name: "category",
          description: "Lists every registration in one category, paginated (public GET)",
          schema: z.object({ q: z.string(), limit: z.number().optional(), offset: z.number().optional() }),
        },
      ),
      tool(
        async (input) => this.client.findServicesByCapability(input),
        {
          name: "findServicesByCapability",
          description: "Ranks registered services/tools by relevance to a free-text query",
          schema: z.object({ query: z.string(), top_k: z.number().optional() }),
        },
      ),
      tool(
        async (input) => this.client.search(input),
        {
          name: "search",
          description: "Ranks registered services/tools by relevance to a free-text query (public GET)",
          schema: z.object({ q: z.string(), category: z.string().nullable().optional(), limit: z.number().optional() }),
        },
      ),
    ];
  }
}
