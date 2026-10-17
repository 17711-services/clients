"""Pydantic request/response models for token-verdict-service."""

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class ContractInfo(BaseModel):
    blacklist: Optional[bool] = None  # Whether the contract can block addresses.
    hidden_owner: Optional[bool] = None  # Whether the real owner is hidden.
    mintable: Optional[bool] = None  # Whether new tokens can be minted.
    owner: Optional[str] = None  # Owner address, absent when ownership is renounced.
    owner_can_reclaim: Optional[bool] = None  # Whether a previous owner can take ownership back.
    ownership_renounced: bool
    pausable: Optional[bool] = None  # Whether transfers can be paused.
    proxy: Optional[bool] = None  # Whether it is an upgradeable proxy (the logic can be replaced).
    self_destruct: Optional[bool] = None  # Whether the contract can self-destruct.
    source_verified: Optional[bool] = None  # Whether the source code is published and verified.
    taxes_modifiable: Optional[bool] = None  # Whether the owner can change the taxes after launch.

    @classmethod
    def _dummy(cls) -> "ContractInfo":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(blacklist=None, hidden_owner=None, mintable=None, owner=None, owner_can_reclaim=None, ownership_renounced=False, pausable=None, proxy=None, self_destruct=None, source_verified=None, taxes_modifiable=None)


class Finding(BaseModel):
    code: str  # Stable code, e.g. `trading.honeypot`, `liquidity.low`, `contract.mintable`.
    message: str
    severity: str  # `critical`, `high`, `medium`, `low` or `info`.

    @classmethod
    def _dummy(cls) -> "Finding":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(code="test", message="test", severity="test")


class HoldersInfo(BaseModel):
    count: Optional[int] = None
    creator_percent: Optional[float] = None  # Share of the supply held by the creator, in percent.
    owner_percent: Optional[float] = None  # Share of the supply held by the owner, in percent.
    top10_wallets_percent: Optional[float] = None  # Share held by the ten largest wallets that are not contracts, in percent.

    @classmethod
    def _dummy(cls) -> "HoldersInfo":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(count=None, creator_percent=None, owner_percent=None, top10_wallets_percent=None)


class LiquidityInfo(BaseModel):
    locked_percent: Optional[float] = None  # Share of the liquidity-token supply that is locked, in percent.
    pool_age_days: Optional[float] = None  # Age in days of the oldest trading pool.
    pools: int
    top_pool: Optional[str] = None  # Largest pool: exchange name.
    total_usd: float  # Liquidity in USD summed over the trading pools.

    @classmethod
    def _dummy(cls) -> "LiquidityInfo":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(locked_percent=None, pool_age_days=None, pools=0, top_pool=None, total_usd=0.0)


class MarketInfo(BaseModel):
    buys_24h: int
    fully_diluted_value_usd: Optional[float] = None
    price_change_24h_percent: Optional[float] = None
    price_usd: Optional[float] = None
    sells_24h: int
    volume_24h_usd: float

    @classmethod
    def _dummy(cls) -> "MarketInfo":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(buys_24h=0, fully_diluted_value_usd=None, price_change_24h_percent=None, price_usd=None, sells_24h=0, volume_24h_usd=0.0)


class TradingInfo(BaseModel):
    buy_tax_percent: Optional[float] = None  # Buy tax in percent.
    cannot_sell_all: Optional[bool] = None  # Whether a holder cannot sell their whole balance.
    honeypot: Optional[bool] = None  # Whether the token cannot be sold after being bought.
    sell_tax_percent: Optional[float] = None  # Sell tax in percent.

    @classmethod
    def _dummy(cls) -> "TradingInfo":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(buy_tax_percent=None, cannot_sell_all=None, honeypot=None, sell_tax_percent=None)


class GetVerdictResponse(BaseModel):
    address: str
    age_seconds: int  # How old this verdict is, in seconds (0 for a fresh check).
    chain: str
    contract: ContractInfo
    disclaimer: str  # Always states that this is an automated risk screen, not advice.
    findings: List[Finding]  # Everything that drove the verdict, most severe first.
    from_cache: bool  # `true` when served from a stored result.
    holders: HoldersInfo
    liquidity: LiquidityInfo
    market: MarketInfo
    name: Optional[str] = None
    retrieved_at: str  # When the data was read (UTC).
    safety_score: int  # 0 to 100, higher is safer; derived from the findings.
    sources: List[str]  # The data sources consulted.
    symbol: Optional[str] = None
    trading: TradingInfo
    verdict: str  # `safe`, `caution`, `danger` or `unknown` (the security source did not answer: not a green light).

    @classmethod
    def _dummy(cls) -> "GetVerdictResponse":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(address="test", age_seconds=0, chain="test", contract=ContractInfo._dummy(), disclaimer="test", findings=[], from_cache=False, holders=HoldersInfo._dummy(), liquidity=LiquidityInfo._dummy(), market=MarketInfo._dummy(), name=None, retrieved_at="test", safety_score=0, sources=[], symbol=None, trading=TradingInfo._dummy(), verdict="test")


class GetVerdictRequest(BaseModel):
    address: str  # The token contract address (`0x` followed by 40 hex characters).
    chain: Optional[str] = None  # The chain: `base` (default), `ethereum`, `bsc`, `polygon`, `arbitrum`, `optimism` or `avalanche`.
    max_age_seconds: Optional[int] = None  # The oldest verdict you accept, in seconds. Omit it for the default (verdicts up to 5 minutes old); `0` forces a fresh check. The response always says how old it is.

    @classmethod
    def _dummy(cls) -> "GetVerdictRequest":
        """A minimal, always-constructible instance -- test fixtures only, never real data."""
        return cls(address="test", chain=None, max_age_seconds=None)
