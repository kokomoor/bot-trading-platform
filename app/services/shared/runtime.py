from __future__ import annotations

from app.infrastructure.adapters import SimulationAdapter
from app.services.execution_engine.engine import ExecutionEngine
from app.services.execution_engine.risk_engine import RiskEngine, RiskLimits
from app.services.shared.platform_state import platform_state

risk_engine = RiskEngine(
    limits=RiskLimits(
        per_strategy_notional_limit=50_000,
        per_account_notional_limit=100_000,
        max_position_size=20,
        allowed_symbols={"BTC-USD"},
    )
)
execution_engine = ExecutionEngine(
    adapter=SimulationAdapter(),
    risk_engine=risk_engine,
    state=platform_state,
)


def set_kill_switch(enabled: bool) -> None:
    platform_state.kill_switch_enabled = enabled
    risk_engine.set_kill_switch(enabled)


async def adapter_health_summary() -> dict[str, bool]:
    return {
        "simulation": await execution_engine.adapter.healthcheck(),
        "kraken_like": False,
        "ibkr_like": False,
    }


def startup_checks() -> dict[str, object]:
    recovered = execution_engine.startup_recovery()
    return {
        "recovered_pending_orders": recovered,
        "kill_switch_enabled": platform_state.kill_switch_enabled,
    }
