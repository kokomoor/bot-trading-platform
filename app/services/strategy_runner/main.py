"""Strategy runner placeholder service."""

import asyncio

from app.core.logging import get_logger
from app.services.shared.platform_state import platform_state
from app.services.shared.runtime import execution_engine
from app.services.simulation.feed import SimulatedMarketFeed
from app.services.strategy_runner.examples import (
    MovingAverageCrossStrategy,
    ThresholdReversionStrategy,
)
from app.services.strategy_runner.runner import StrategyRunner
from app.services.strategy_runner.strategy import StrategyRuntimeMetadata

logger = get_logger(service="strategy_runner")


async def run_once() -> None:
    logger.info("strategy_runner.startup")
    platform_state.strategies["ma_cross"] = {"name": "Moving Average Cross"}
    platform_state.strategies["threshold_reversion"] = {"name": "Threshold Reversion"}

    ma_strategy = MovingAverageCrossStrategy(
        metadata=StrategyRuntimeMetadata(
            strategy_id="ma_cross",
            deployment_id="deploy_ma_cross",
            code_version="1.0.0",
            config_version="1",
            account_id="paper-account-1",
            venue="sim",
        )
    )
    threshold_strategy = ThresholdReversionStrategy(
        metadata=StrategyRuntimeMetadata(
            strategy_id="threshold_reversion",
            deployment_id="deploy_threshold_reversion",
            code_version="1.0.0",
            config_version="1",
            account_id="paper-account-1",
            venue="sim",
        ),
        anchor_price=100.0,
    )

    runner = StrategyRunner(strategies=[ma_strategy, threshold_strategy])
    feed = SimulatedMarketFeed(symbol="BTC-USD", seed_price=100.0, step=1.0, length=30)
    for tick in feed.stream():
        intents = runner.process_tick(tick)
        for intent in intents:
            await execution_engine.submit_intent(intent, reference_price=tick.price)

    logger.info(
        "strategy_runner.completed",
        orders=len(platform_state.orders),
        events=len(platform_state.events),
    )


def run() -> None:
    asyncio.run(run_once())


if __name__ == "__main__":
    run()
