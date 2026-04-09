import pytest

from app.infrastructure.adapters import SimulationAdapter
from app.services.execution_engine.engine import ExecutionEngine
from app.services.execution_engine.risk_engine import RiskEngine, RiskLimits
from app.services.shared.platform_state import PlatformState
from app.services.strategy_runner.strategy import StrategyIntent


@pytest.mark.asyncio
async def test_execution_e2e_updates_orders_positions_balances() -> None:
    state = PlatformState()
    risk = RiskEngine(
        limits=RiskLimits(
            per_strategy_notional_limit=100_000,
            per_account_notional_limit=100_000,
            max_position_size=10,
            allowed_symbols={"BTC-USD"},
        )
    )
    engine = ExecutionEngine(adapter=SimulationAdapter(), risk_engine=risk, state=state)
    intent = StrategyIntent(
        strategy_id="strat-1",
        deployment_id="deploy-1",
        account_id="acct-1",
        venue="sim",
        symbol="BTC-USD",
        side="buy",
        quantity=1.0,
        idempotency_key="idem-1",
    )

    decision = await engine.submit_intent(intent, reference_price=100.0)

    assert decision.approved
    assert state.orders
    assert state.positions[("acct-1", "BTC-USD")].quantity == 1.0
    assert state.balances[("acct-1", "USD")].total < 1_000_000


@pytest.mark.asyncio
async def test_kill_switch_blocks_new_intents() -> None:
    state = PlatformState(kill_switch_enabled=True)
    risk = RiskEngine(
        limits=RiskLimits(
            per_strategy_notional_limit=100_000,
            per_account_notional_limit=100_000,
            max_position_size=10,
        ),
        kill_switch_enabled=True,
    )
    engine = ExecutionEngine(adapter=SimulationAdapter(), risk_engine=risk, state=state)
    intent = StrategyIntent(
        strategy_id="strat-1",
        deployment_id="deploy-1",
        account_id="acct-1",
        venue="sim",
        symbol="BTC-USD",
        side="buy",
        quantity=1.0,
        idempotency_key="idem-2",
    )

    decision = await engine.submit_intent(intent, reference_price=100.0)

    assert not decision.approved
    assert not state.orders
