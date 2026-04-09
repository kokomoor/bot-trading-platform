from app.services.execution_engine.risk_engine import RiskEngine, RiskLimits
from app.services.strategy_runner.strategy import StrategyIntent


def _intent(symbol: str = "BTC-USD", qty: float = 1.0) -> StrategyIntent:
    return StrategyIntent(
        strategy_id="strat-1",
        deployment_id="deploy-1",
        account_id="acct-1",
        venue="sim",
        symbol=symbol,
        side="buy",
        quantity=qty,
        idempotency_key="idem-1",
    )


def test_risk_engine_approves_within_limits() -> None:
    engine = RiskEngine(
        limits=RiskLimits(
            per_strategy_notional_limit=10_000,
            per_account_notional_limit=10_000,
            max_position_size=10,
            allowed_symbols={"BTC-USD"},
        )
    )
    decision = engine.evaluate(_intent(), reference_price=100)
    assert decision.approved


def test_risk_engine_rejects_on_kill_switch() -> None:
    engine = RiskEngine(
        limits=RiskLimits(
            per_strategy_notional_limit=10_000,
            per_account_notional_limit=10_000,
            max_position_size=10,
        ),
        kill_switch_enabled=True,
    )
    decision = engine.evaluate(_intent(), reference_price=100)
    assert not decision.approved
    assert decision.reason == "kill_switch_enabled"


def test_risk_engine_rejects_denied_symbol() -> None:
    engine = RiskEngine(
        limits=RiskLimits(
            per_strategy_notional_limit=10_000,
            per_account_notional_limit=10_000,
            max_position_size=10,
            denied_symbols={"BTC-USD"},
        )
    )
    decision = engine.evaluate(_intent(), reference_price=100)
    assert not decision.approved
