/**
 * Typed HTTP client and request/response interfaces for extract-correct-service.
 */

import { Client as BaseClient, type ClientOptions } from "@xyz17711/core";

/** One deterministic correction actually applied to the extracted value. */
export interface AppliedFix {
  /** Human-readable detail of what changed. */
  detail: string;
  /** JSON Pointer to the field that was corrected (e.g. `/user/age`; `""` = the whole value). */
  path: string;
  /** Which bounded correction rule fired (e.g. `type_coercion`, `additional_property_stripped`, `enum_case_insensitive_match`, `required_default_filled`, `clamped_to_minimum`, `clamped_to_maximum`, `array_truncated_to_max_items`). */
  rule: string;
}

/** One schema violation that could NOT be corrected -- never silently dropped or guessed. */
export interface RemainingIssue {
  /** The JSON Schema keyword that failed (e.g. `pattern`, `format`, `minItems`, `oneOf`). */
  keyword: string;
  /** The underlying validator's own error message. */
  message: string;
  /** JSON Pointer to the field that still fails validation. */
  path: string;
}

export interface ParseJsonResponse {
  /** Every correction actually applied, in the order applied. */
  applied_fixes: AppliedFix[];
  /** The extracted (and, if a schema was supplied, corrected) JSON value. */
  data: unknown;
  /** How `data` was obtained: `"direct"` (already valid JSON), `"repaired"` (malformed JSON fixed in place), or `"extracted_and_repaired"` (isolated from surrounding text, then fixed). */
  extraction_method: string;
  /** Every schema violation that remains after correction -- non-empty only when `schema` was supplied and at least one issue couldn't be fixed by a bounded v1 rule. */
  remaining_issues: RemainingIssue[];
  /** Whether `data` satisfies `schema` after correction. `None` when no `schema` was supplied -- never conflated with "assumed valid". */
  valid?: boolean | null;
}

export interface ParseJsonRequest {
  /** Optional JSON Schema to validate the extracted value against and auto-correct where a bounded, deterministic fix rule applies. Omitted = extraction only, no validation. */
  schema?: unknown;
  /** Free-form or messy text to extract structured JSON from -- already-valid JSON, JSON wrapped in prose or a markdown code fence, or malformed JSON (trailing commas, single-quoted strings, unquoted keys, a truncated array/object). */
  text: string;
}

/** Production base URL of this service; pass another to self-host or test. */
export const DEFAULT_BASE_URL = "https://api.17711.xyz/registry/extract-correct-service";

/** Typed client for extract-correct-service, e.g. `client.parseJson(...)`. */
export class Client extends BaseClient {
  /**
   * `new Client()` talks to the production service. Pass a base URL to target another
   * instance, and/or wallet options (`new Client({ x402PrivateKey, ... })`) to pay past the
   * free quota automatically.
   */
  constructor(options?: ClientOptions);
  constructor(baseUrl?: string, options?: ClientOptions);
  constructor(baseUrlOrOptions?: string | ClientOptions, options: ClientOptions = {}) {
    const [url, opts]: [string, ClientOptions] =
      typeof baseUrlOrOptions === "object"
        ? [DEFAULT_BASE_URL, baseUrlOrOptions]
        : [baseUrlOrOptions ?? DEFAULT_BASE_URL, options];
    super(url, opts);
  }

  /** JSON repair API: extract valid JSON from messy text or model output and fix it against a JSON Schema ($0.006, x402) */
  async parseJson(request: ParseJsonRequest): Promise<ParseJsonResponse> {
    return this.post<ParseJsonResponse>("/v1/extract-correct/parse_json", request);
  }
}

export { ClientOptions };
