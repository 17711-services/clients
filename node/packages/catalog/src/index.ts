/**
 * Typed HTTP client and request/response interfaces for catalog.
 */

import { Client as BaseClient, type ClientOptions } from "@xyz17711/core";

export interface CatalogCategoryEntry {
  category: string;
  description: string;
  host: string;
  name: string;
  port: number;
  registered_at: number;
}

export interface CatalogCategoryResponse {
  /** This page's entries, in no particular order (no ranking -- this is a listing, not a search). */
  entries: CatalogCategoryEntry[];
  limit: number;
  offset: number;
  /** Total number of registrations matching `q`, BEFORE `limit`/`offset` are applied -- lets a caller know whether more pages remain. */
  total_count: number;
}

export interface SearchResult {
  description: string;
  host: string;
  method: string;
  port: number;
  /** Decimal USDC string (e.g. `"0.01"`), or `""` if this tool is free -- structural pricing, not just prose in `description`. */
  price_usdc: string;
  route: string;
  /** Similarity score (semantic embedding cosine similarity when available, else keyword overlap in `[0, 1]`) -- higher is a better match. Not comparable across two different searches (the scoring method may differ per-call depending on embedding availability). */
  score: number;
  service_name: string;
  tool_name: string;
}

export interface SearchResponse {
  /** Ranked best-match-first, truncated to the request's own `top_k`. */
  results: SearchResult[];
}

export interface SearchRequest {
  /** Free-text description of the task to find a service for. */
  query: string;
  /** Max number of results to return. */
  top_k?: number;
}

export interface CatalogSearchResult {
  category: string;
  description: string;
  host: string;
  method: string;
  port: number;
  /** Decimal USDC string (e.g. `"0.01"`), or `""` if this tool is free -- structural pricing, not just prose in `description`. */
  price_usdc: string;
  route: string;
  /** Similarity score (semantic embedding cosine similarity when available, else keyword overlap in `[0, 1]`) -- higher is a better match. Not comparable across two different searches (the scoring method may differ per-call depending on embedding availability). */
  score: number;
  service_name: string;
  tool_name: string;
}

export interface CatalogSearchResponse {
  /** Ranked best-match-first, truncated to the request's own `limit`. */
  results: CatalogSearchResult[];
}

/** Typed client for catalog, e.g. `client.category(...)`. */
export class Client extends BaseClient {
  /** Lists every registration in one category, paginated (public GET) */
  async category(params: { q: string; limit?: number; offset?: number }): Promise<CatalogCategoryResponse> {
    return this.get<CatalogCategoryResponse>("/v1/catalog/category", { q: params.q, limit: params.limit, offset: params.offset });
  }

  /** Ranks registered services/tools by relevance to a free-text query */
  async findServicesByCapability(request: SearchRequest): Promise<SearchResponse> {
    return this.post<SearchResponse>("/v1/catalog/find_services_by_capability", request);
  }

  /** Ranks registered services/tools by relevance to a free-text query (public GET) */
  async search(params: { q: string; category?: string | null; limit?: number }): Promise<CatalogSearchResponse> {
    return this.get<CatalogSearchResponse>("/v1/catalog/search", { q: params.q, category: params.category, limit: params.limit });
  }
}

export { ClientOptions };
