/**
 * Typed HTTP client and request/response interfaces for token-verdict-service.
 */

import { Client as BaseClient, type ClientOptions } from "@xyz17711/core";

export interface ContractInfo {
  /** Whether the contract can block addresses. */
  blacklist?: boolean | null;
  /** Whether the real owner is hidden. */
  hidden_owner?: boolean | null;
  /** Whether new tokens can be minted. */
  mintable?: boolean | null;
  /** Owner address, absent when ownership is renounced. */
  owner?: string | null;
  /** Whether a previous owner can take ownership back. */
  owner_can_reclaim?: boolean | null;
  ownership_renounced: boolean;
  /** Whether transfers can be paused. */
  pausable?: boolean | null;
  /** Whether it is an upgradeable proxy (the logic can be replaced). */
  proxy?: boolean | null;
  /** Whether the contract can self-destruct. */
  self_destruct?: boolean | null;
  /** Whether the source code is published and verified. */
  source_verified?: boolean | null;
  /** Whether the owner can change the taxes after launch. */
  taxes_modifiable?: boolean | null;
}

export interface Finding {
  /** Stable code, e.g. `trading.honeypot`, `liquidity.low`, `contract.mintable`. */
  code: string;
  message: string;
  /** `critical`, `high`, `medium`, `low` or `info`. */
  severity: string;
}

export interface HoldersInfo {
  count?: number | null;
  /** Share of the supply held by the creator, in percent. */
  creator_percent?: number | null;
  /** Share of the supply held by the owner, in percent. */
  owner_percent?: number | null;
  /** Share held by the ten largest wallets that are not contracts, in percent. */
  top10_wallets_percent?: number | null;
}

export interface LiquidityInfo {
  /** Share of the liquidity-token supply that is locked, in percent. */
  locked_percent?: number | null;
  /** Age in days of the oldest trading pool. */
  pool_age_days?: number | null;
  pools: number;
  /** Largest pool: exchange name. */
  top_pool?: string | null;
  /** Liquidity in USD summed over the trading pools. */
  total_usd: number;
}

export interface MarketInfo {
  buys_24h: number;
  fully_diluted_value_usd?: number | null;
  price_change_24h_percent?: number | null;
  price_usd?: number | null;
  sells_24h: number;
  volume_24h_usd: number;
}

export interface TradingInfo {
  /** Buy tax in percent. */
  buy_tax_percent?: number | null;
  /** Whether a holder cannot sell their whole balance. */
  cannot_sell_all?: boolean | null;
  /** Whether the token cannot be sold after being bought. */
  honeypot?: boolean | null;
  /** Sell tax in percent. */
  sell_tax_percent?: number | null;
}

export interface GetVerdictResponse {
  address: string;
  /** How old this verdict is, in seconds (0 for a fresh check). */
  age_seconds: number;
  chain: string;
  contract: ContractInfo;
  /** Always states that this is an automated risk screen, not advice. */
  disclaimer: string;
  /** Everything that drove the verdict, most severe first. */
  findings: Finding[];
  /** `true` when served from a stored result. */
  from_cache: boolean;
  holders: HoldersInfo;
  liquidity: LiquidityInfo;
  market: MarketInfo;
  name?: string | null;
  /** When the data was read (UTC). */
  retrieved_at: string;
  /** 0 to 100, higher is safer; derived from the findings. */
  safety_score: number;
  /** The data sources consulted. */
  sources: string[];
  symbol?: string | null;
  trading: TradingInfo;
  /** `safe`, `caution`, `danger` or `unknown` (the security source did not answer: not a green light). */
  verdict: string;
}

export interface GetVerdictRequest {
  /** The token contract address (`0x` followed by 40 hex characters). */
  address: string;
  /** The chain: `base` (default), `ethereum`, `bsc`, `polygon`, `arbitrum`, `optimism` or `avalanche`. */
  chain?: string | null;
  /** The oldest verdict you accept, in seconds. Omit it for the default (verdicts up to 5 minutes old); `0` forces a fresh check. The response always says how old it is. */
  max_age_seconds?: number | null;
}

/** Typed client for token-verdict-service, e.g. `client.getVerdict(...)`. */
export class Client extends BaseClient {
  /** Token verdict and security check: is this token safe? Honeypot, rug pull and scam detection with taxes, liquidity and admin powers ($0.01, x402) */
  async getVerdict(request: GetVerdictRequest): Promise<GetVerdictResponse> {
    return this.post<GetVerdictResponse>("/v1/token-verdict/get_verdict", request);
  }
}

export { ClientOptions };
