/**
 * LangChain.js tools for websearch, grouped in one Toolkit -- one tool per operation, each just an async function (JS has no separate sync form to generate). Requires the `@langchain/core`+`zod` peer dependencies declared in this package's own package.json -- imported from `websearch/langchain`, never from the package root, so importing the base client never requires them installed.
 */

import { tool } from "@langchain/core/tools";
import { z } from "zod";
import { Client } from "./index.js";

export class WebsearchToolkit {
  private client: Client;

  constructor(client: Client) {
    this.client = client;
  }

  getTools() {
    return [
      tool(
        async (input) => this.client.getTaskStatus(input),
        {
          name: "getTaskStatus",
          description: "Polls for the result of a task enqueued by a *_async tool",
          schema: z.object({ task_id: z.string() }),
        },
      ),
      tool(
        async (input) => this.client.searchWeb(input),
        {
          name: "searchWeb",
          description: "Web search API for agents: search the web and get result titles, URLs and snippets as JSON ($0.005, x402)",
          schema: z.object({ query: z.string() }),
        },
      ),
      tool(
        async (input) => this.client.searchWebAsync(input),
        {
          name: "searchWebAsync",
          description: "[Deprecated - use websearch_search_web] Enqueues a websearch_search_web job and returns a task id immediately ($0.005, x402)",
          schema: z.object({ callback_url: z.string().nullable().optional(), query: z.string() }),
        },
      ),
    ];
  }
}
