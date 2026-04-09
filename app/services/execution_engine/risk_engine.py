from __future__ import annotations

from dataclasses import dataclass, field

from app.services.strategy_runner.strategy import StrategyIntent


@dataclass(frozen=True, slots=True)
class RiskLimits:
    per_strategy_notional_limit: float
    per_account_notional_limit: float
    max_position_size: float
    allowed_symbols: set[str] = field(default_factory=set)
    denied_symbols: set[str] = field(default_factory=set)


@dataclass(frozen=True, slots=True)
class RiskDecision:
    approved: bool
    reason: str
    resized_quantity: float | None = None


@dataclass(slots=True)
class RiskEngine:
    limits: RiskLimits
    kill_switch_enabled: bool = False
    strategy_notional_usage: dict[str, float] = field(default_factory=dict)
    account_notional_usage: dict[str, float] = field(default_factory=dict)
    position_size: dict[tuple[str, str], float] = field(default_factory=dict)

    def set_kill_switch(self, enabled: bool) -> None:
        self.kill_switch_enabled = enabled

    def evaluate(self, intent: StrategyIntent, reference_price: float) -> RiskDecision:
        if self.kill_switch_enabled:
            return RiskDecision(approved=False, reason="kill_switch_enabled")

        symbol = intent.symbol
        if self.limits.allowed_symbols and symbol not in self.limits.allowed_symbols:
            return RiskDecision(approved=False, reason="symbol_not_allowed")
        if symbol in self.limits.denied_symbols:
            return RiskDecision(approved=False, reason="symbol_denied")

        notional = abs(intent.quantity * reference_price)
        strategy_used = self.strategy_notional_usage.get(intent.strategy_id, 0.0)
        account_used = self.account_notional_usage.get(intent.account_id, 0.0)

        if strategy_used + notional > self.limits.per_strategy_notional_limit:
            return RiskDecision(approved=False, reason="strategy_notional_limit_exceeded")
        if account_used + notional > self.limits.per_account_notional_limit:
            return RiskDecision(approved=False, reason="account_notional_limit_exceeded")

        position_key = (intent.account_id, symbol)
        current_position = self.position_size.get(position_key, 0.0)
        side_multiplier = 1.0 if intent.side == "buy" else -1.0
        next_position = current_position + (intent.quantity * side_multiplier)

        if abs(next_position) > self.limits.max_position_size:
            return RiskDecision(approved=False, reason="max_position_size_exceeded")

        self.strategy_notional_usage[intent.strategy_id] = strategy_used + notional
        self.account_notional_usage[intent.account_id] = account_used + notional
        self.position_size[position_key] = next_position
        return RiskDecision(approved=True, reason="approved")
