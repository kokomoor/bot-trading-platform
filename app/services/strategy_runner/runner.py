from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from app.domain.market_data import MarketTick
from app.services.strategy_runner.strategy import Strategy, StrategyIntent


@dataclass(slots=True)
class StrategyRunner:
    strategies: list[Strategy]
    enabled_strategies: set[str] | None = None

    def process_tick(self, tick: MarketTick) -> list[StrategyIntent]:
        intents: list[StrategyIntent] = []
        for strategy in self.strategies:
            if (
                self.enabled_strategies is not None
                and strategy.metadata.strategy_id not in self.enabled_strategies
            ):
                continue
            intent = strategy.on_tick(tick)
            if intent is not None:
                intents.append(intent)
        return intents

    def process_feed(self, ticks: Iterable[MarketTick]) -> list[StrategyIntent]:
        all_intents: list[StrategyIntent] = []
        for tick in ticks:
            all_intents.extend(self.process_tick(tick))
        return all_intents
