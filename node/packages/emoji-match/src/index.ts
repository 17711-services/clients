/**
 * Typed HTTP client and request/response interfaces for emoji-match-service.
 */

import { Client as BaseClient, type ClientOptions } from "@xyz17711/core";

export interface SuggestEmojisResponse {
  /** 1 to 5 emoji matching the text's lexicon/meaning, most relevant first. */
  emojis: string[];
  /** Which language (ISO 639-1 code, e.g. "en"/"fr") the best match was found in -- the input is stemmed and scored against every supported language, and this reports which one actually produced the result, useful to gauge match confidence for an unfamiliar language. */
  matched_language: string;
}

export interface SuggestEmojisRequest {
  /** The text to analyze. Works best in English or French; best-effort for 16 other languages (see the tool's own description). Truncated to a reasonable length before analysis if very long -- the response reflects the truncated text, not the full input. */
  text: string;
}

/** Typed client for emoji-match-service, e.g. `client.suggestEmojis(...)`. */
export class Client extends BaseClient {
  /** Suggests 1-5 emoji matching a text's lexicon, English/French best-supported ($0.001, x402) */
  async suggestEmojis(request: SuggestEmojisRequest): Promise<SuggestEmojisResponse> {
    return this.post<SuggestEmojisResponse>("/v1/emoji-match/suggest_emojis", request);
  }
}

export { ClientOptions };
