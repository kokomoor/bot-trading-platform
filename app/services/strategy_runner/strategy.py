from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from app.domain.market_data import MarketTick


@dataclass(frozen=True, slots=True)
class StrategyRuntimeMetadata:
    strategy_id: str
    deployment_id: str
    code_version: str
    config_version: str
    account_id: str
    venue: str


@dataclass(frozen=True, slots=True)
class StrategyIntent:
    strategy_id: str
    deployment_id: str
    account_id: str
    venue: str
    symbol: str
    side: str
    quantity: float
    idempotency_key: str


class Strategy(Protocol):
    metadata: StrategyRuntimeMetadata

    def on_tick(self, tick: MarketTick) -> StrategyIntent | None: ...
