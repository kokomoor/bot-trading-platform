from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field

from app.core.ids import new_idempotency_key
from app.domain.market_data import MarketTick
from app.services.strategy_runner.strategy import Strategy, StrategyIntent, StrategyRuntimeMetadata


@dataclass(slots=True)
class MovingAverageCrossStrategy(Strategy):
    metadata: StrategyRuntimeMetadata
    short_window: int = 3
    long_window: int = 5
    _prices: deque[float] = field(default_factory=lambda: deque(maxlen=50))

    def on_tick(self, tick: MarketTick) -> StrategyIntent | None:
        self._prices.append(tick.price)
        if len(self._prices) < self.long_window:
            return None

        short_avg = sum(list(self._prices)[-self.short_window :]) / self.short_window
        long_avg = sum(list(self._prices)[-self.long_window :]) / self.long_window

        if short_avg > long_avg:
            return self._intent(symbol=tick.symbol, side="buy", quantity=1.0)
        if short_avg < long_avg:
            return self._intent(symbol=tick.symbol, side="sell", quantity=1.0)
        return None

    def _intent(self, *, symbol: str, side: str, quantity: float) -> StrategyIntent:
        return StrategyIntent(
            strategy_id=self.metadata.strategy_id,
            deployment_id=self.metadata.deployment_id,
            account_id=self.metadata.account_id,
            venue=self.metadata.venue,
            symbol=symbol,
            side=side,
            quantity=quantity,
            idempotency_key=new_idempotency_key(self.metadata.strategy_id),
        )


@dataclass(slots=True)
class ThresholdReversionStrategy(Strategy):
    metadata: StrategyRuntimeMetadata
    anchor_price: float
    threshold_pct: float = 0.01

    def on_tick(self, tick: MarketTick) -> StrategyIntent | None:
        lower = self.anchor_price * (1 - self.threshold_pct)
        upper = self.anchor_price * (1 + self.threshold_pct)
        if tick.price <= lower:
            return self._intent(symbol=tick.symbol, side="buy", quantity=0.5)
        if tick.price >= upper:
            return self._intent(symbol=tick.symbol, side="sell", quantity=0.5)
        return None

    def _intent(self, *, symbol: str, side: str, quantity: float) -> StrategyIntent:
        return StrategyIntent(
            strategy_id=self.metadata.strategy_id,
            deployment_id=self.metadata.deployment_id,
            account_id=self.metadata.account_id,
            venue=self.metadata.venue,
            symbol=symbol,
            side=side,
            quantity=quantity,
            idempotency_key=new_idempotency_key(self.metadata.strategy_id),
        )
