/**
 * Typed HTTP client and request/response interfaces for web-scraper.
 */

import { Client as BaseClient, type ClientOptions } from "@xyz17711/core";

export interface ExtractMarkdownResponse {
  content_type?: string | null;
  /** The URL actually reached, after any redirects the target sent. */
  final_url: string;
  /** Boilerplate-stripped main article content, as Markdown -- navigation, ads, and sidebars removed, not the raw page HTML. */
  markdown: string;
  /** The REAL HTTP status the underlying fetch received. */
  status: number;
  /** Article title, if Readability found one. */
  title?: string | null;
  /** `true` if the underlying fetch's HTML was truncated by web-scraper's own fixed byte ceiling (see `web_scraper_scrape_url`'s own `truncated` field) -- `markdown` may then also be incomplete. */
  truncated: boolean;
  /** The URL as requested, verbatim. */
  url: string;
}

export interface ExtractMarkdownRequest {
  /** The target URL to fetch, e.g. `"https://example.com/article"`. Must be `http://` or `https://` -- same validation as `web_scraper_scrape_url`, since this tool fetches through the exact same internal scraper. */
  url: string;
}

/** `"pending"` (enqueued, no result yet), `"finished"` (a worker wrote a result -- see `ok`/ `result`), or `"unknown"` (this id was never valid, or both it and its result have expired -- see [`nimpoleon_tasks::TaskState`]'s own doc comment for why this is 3 states, not 2). */
export interface TaskStatusKind {
}

export interface GetTaskStatusResponse {
  ok?: boolean | null;
  result?: unknown;
  status: TaskStatusKind;
}

export interface GetTaskStatusRequest {
  /** The `task_id` a `*_async` tool returned. */
  task_id: string;
}

export interface ScrapeUrlResponse {
  content_type?: string | null;
  /** The URL actually reached, after any redirects the target sent. */
  final_url: string;
  /** Raw response body, decoded as UTF-8 (lossy -- see this tool's own description for why), truncated to this service's own fixed byte ceiling if needed. */
  html: string;
  /** The REAL HTTP status the target returned -- never masked, never itself a reason to retry. */
  status: number;
  /** `true` if `html` was cut short by this service's own fixed byte ceiling. */
  truncated: boolean;
  /** The URL as requested, verbatim. */
  url: string;
}

export interface ScrapeUrlRequest {
  /** The target URL to fetch, e.g. `"https://example.com/page"`. Must be `http://` or `https://` -- any other scheme is rejected before any fetch is attempted. */
  url: string;
}

/** The fixed response shape of every `*_async` tool -- deliberately NOT generic over the underlying sync tool's own response type, since no work has actually happened yet at this point. */
export interface AsyncTaskResponse {
  task_id: string;
}

export interface ScrapeUrlAsyncRequest {
  /** When set, the worker that processes this task POSTs the eventual result (a `TaskResult` JSON body) here, best-effort -- polling `web_scraper_get_task_status` always works too, regardless of whether this is set. */
  callback_url?: string | null;
  /** The target URL to fetch, e.g. `"https://example.com/page"`. Must be `http://` or `https://` -- any other scheme is rejected before any fetch is attempted. */
  url: string;
}

/** Typed client for web-scraper, e.g. `client.extractMarkdown(...)`. */
export class Client extends BaseClient {
  /** URL to Markdown: read any web page and get its main article content as clean Markdown for agents ($0.003, x402) */
  async extractMarkdown(request: ExtractMarkdownRequest): Promise<ExtractMarkdownResponse> {
    return this.post<ExtractMarkdownResponse>("/v1/web-scraper/extract_markdown", request);
  }

  /** Polls for the result of a task enqueued by a *_async tool */
  async getTaskStatus(request: GetTaskStatusRequest): Promise<GetTaskStatusResponse> {
    return this.post<GetTaskStatusResponse>("/v1/web-scraper/get_task_status", request);
  }

  /** Scrape URL: fetch any web page through a proxy and get its status, content type and raw HTML ($0.002, x402) */
  async scrapeUrl(request: ScrapeUrlRequest): Promise<ScrapeUrlResponse> {
    return this.post<ScrapeUrlResponse>("/v1/web-scraper/scrape_url", request);
  }

  /** [Deprecated - use web_scraper_scrape_url] Enqueues a web_scraper_scrape_url job and returns a task id immediately ($0.002, x402) */
  async scrapeUrlAsync(request: ScrapeUrlAsyncRequest): Promise<AsyncTaskResponse> {
    return this.post<AsyncTaskResponse>("/v1/web-scraper/scrape_url_async", request);
  }
}

export { ClientOptions };
