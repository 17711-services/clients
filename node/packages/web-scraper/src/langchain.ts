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
          description: "URL to Markdown: read any web page and get its main article content as clean Markdown for agents ($0.003, x402)",
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
          description: "Scrape URL: fetch any web page through a proxy and get its status, content type and raw HTML ($0.002, x402)",
          schema: z.object({ url: z.string() }),
        },
      ),
      tool(
        async (input) => this.client.scrapeUrlAsync(input),
        {
          name: "scrapeUrlAsync",
          description: "[Deprecated - use web_scraper_scrape_url] Enqueues a web_scraper_scrape_url job and returns a task id immediately ($0.002, x402)",
          schema: z.object({ callback_url: z.string().nullable().optional(), url: z.string() }),
        },
      ),
    ];
  }
}
