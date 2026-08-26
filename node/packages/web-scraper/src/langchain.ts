/**
 * LangChain.js tools for web-scraper, grouped in one Toolkit -- one tool per operation, each just an async function (JS has no separate sync form to generate). Requires the `@langchain/core`+`zod` peer dependencies declared in this package's own package.json -- imported from `web-scraper/langchain`, never from the package root, so importing the base client never requires them installed.
 */

import { tool } from "@langchain/core/tools";
import { z } from "zod";
import { Client } from "./index.js";

export class WebScraperToolkit {
  private client: Client;

  constructor(client: Client) {
    this.client = client;
  }

  getTools() {
    return [
      tool(
        async (input) => this.client.extractMarkdown(input),
        {
          name: "extractMarkdown",
          description: "Fetches a URL and returns its main article content as clean Markdown ($0.007, x402)",
          schema: z.object({ url: z.string() }),
        },
      ),
      tool(
        async (input) => this.client.getTaskStatus(input),
        {
          name: "getTaskStatus",
          description: "Polls for the result of a task enqueued by a *_async tool",
          schema: z.object({ task_id: z.string() }),
        },
      ),
      tool(
        async (input) => this.client.scrapeUrl(input),
        {
          name: "scrapeUrl",
          description: "Fetches an arbitrary URL through a proxy sourced from proxy-pool, never directly ($0.005, x402)",
          schema: z.object({ url: z.string() }),
        },
      ),
      tool(
        async (input) => this.client.scrapeUrlAsync(input),
        {
          name: "scrapeUrlAsync",
          description: "Enqueues a web_scraper_scrape_url job and returns a task id immediately ($0.005, x402)",
          schema: z.object({ callback_url: z.string().nullable().optional(), url: z.string() }),
        },
      ),
    ];
  }
}
