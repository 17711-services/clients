/**
 * Typed HTTP client and request/response interfaces for websearch.
 */

import { Client as BaseClient, type ClientOptions } from "@xyz17711/core";

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

export interface SearchResultItem {
  snippet: string;
  title: string;
  url: string;
}

export interface SearchWebResponse {
  results: SearchResultItem[];
}

export interface SearchWebRequest {
  /** The search query text, e.g. `"rust async runtime comparison"`. */
  query: string;
}

/** The fixed response shape of every `*_async` tool -- deliberately NOT generic over the underlying sync tool's own response type, since no work has actually happened yet at this point. */
export interface AsyncTaskResponse {
  task_id: string;
}

export interface SearchWebAsyncRequest {
  /** When set, the worker that processes this task POSTs the eventual result (a `TaskResult` JSON body) here, best-effort -- polling `websearch_get_task_status` always works too, regardless of whether this is set. */
  callback_url?: string | null;
  /** The search query text, e.g. `"rust async runtime comparison"`. */
  query: string;
}

/** Typed client for websearch, e.g. `client.getTaskStatus(...)`. */
export class Client extends BaseClient {
  /** Polls for the result of a task enqueued by a *_async tool */
  async getTaskStatus(request: GetTaskStatusRequest): Promise<GetTaskStatusResponse> {
    return this.post<GetTaskStatusResponse>("/v1/websearch/get_task_status", request);
  }

  /** Searches the web, always through a free public proxy sourced from proxy-pool ($0.003, x402) */
  async searchWeb(request: SearchWebRequest): Promise<SearchWebResponse> {
    return this.post<SearchWebResponse>("/v1/websearch/search_web", request);
  }

  /** Enqueues a websearch_search_web job and returns a task id immediately ($0.003, x402) */
  async searchWebAsync(request: SearchWebAsyncRequest): Promise<AsyncTaskResponse> {
    return this.post<AsyncTaskResponse>("/v1/websearch/search_web_async", request);
  }
}

export { ClientOptions };
