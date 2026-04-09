from datetime import UTC, datetime

from app.domain.market_data import MarketTick
from app.services.strategy_runner.examples import (
    MovingAverageCrossStrategy,
    ThresholdReversionStrategy,
)
from app.services.strategy_runner.strategy import StrategyRuntimeMetadata


def _metadata(strategy_id: str) -> StrategyRuntimeMetadata:
    return StrategyRuntimeMetadata(
        strategy_id=strategy_id,
        deployment_id=f"deploy-{strategy_id}",
        code_version="1",
        config_version="1",
        account_id="acct-1",
        venue="sim",
    )


def test_threshold_strategy_emits_intent() -> None:
    strategy = ThresholdReversionStrategy(
        metadata=_metadata("thr"),
        anchor_price=100.0,
        threshold_pct=0.01,
    )
    tick = MarketTick(symbol="BTC-USD", price=98.5, timestamp=datetime.now(tz=UTC))

    intent = strategy.on_tick(tick)

    assert intent is not None
    assert intent.side == "buy"


def test_moving_average_strategy_emits_after_window() -> None:
    strategy = MovingAverageCrossStrategy(metadata=_metadata("ma"), short_window=2, long_window=3)
    prices = [100.0, 101.0, 102.0]
    intent = None
    for price in prices:
        intent = strategy.on_tick(
            MarketTick(symbol="BTC-USD", price=price, timestamp=datetime.now(tz=UTC))
        )

    assert intent is not None
