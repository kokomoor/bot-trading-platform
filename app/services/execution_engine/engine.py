from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from app.core.ids import new_uuid_str
from app.domain.events.envelope import build_event_envelope, envelope_to_dict
from app.infrastructure.adapters.base import NormalizedOrderRequest, TradingAdapter
from app.services.execution_engine.risk_engine import RiskDecision, RiskEngine
from app.services.shared.platform_state import BalanceView, OrderView, PlatformState, PositionView
from app.services.strategy_runner.strategy import StrategyIntent


@dataclass(slots=True)
class ExecutionEngine:
    adapter: TradingAdapter
    risk_engine: RiskEngine
    state: PlatformState

    async def submit_intent(self, intent: StrategyIntent, reference_price: float) -> RiskDecision:
        self.state.record_event(
            envelope_to_dict(
                build_event_envelope(
                    event_type="intent.created",
                    event_version=1,
                    aggregate_type="order_intent",
                    aggregate_id=intent.idempotency_key,
                    strategy_id=intent.strategy_id,
                    deployment_id=intent.deployment_id,
                    account_id=intent.account_id,
                    venue=intent.venue,
                    correlation_id=intent.idempotency_key,
                    payload={
                        "symbol": intent.symbol,
                        "side": intent.side,
                        "quantity": intent.quantity,
                    },
                )
            )
        )

        decision = self.risk_engine.evaluate(intent=intent, reference_price=reference_price)
        self.state.record_event(
            envelope_to_dict(
                build_event_envelope(
                    event_type="risk.approved" if decision.approved else "risk.rejected",
                    event_version=1,
                    aggregate_type="order_intent",
                    aggregate_id=intent.idempotency_key,
                    strategy_id=intent.strategy_id,
                    deployment_id=intent.deployment_id,
                    account_id=intent.account_id,
                    venue=intent.venue,
                    correlation_id=intent.idempotency_key,
                    payload={"reason": decision.reason},
                )
            )
        )
        if not decision.approved:
            return decision

        response = await self.adapter.place_order(
            NormalizedOrderRequest(
                account_id=intent.account_id,
                symbol=intent.symbol,
                side=intent.side,
                quantity=intent.quantity,
                price=reference_price,
            )
        )
        order_id = response.order_id or new_uuid_str()
        order = OrderView(
            order_id=order_id,
            intent_id=intent.idempotency_key,
            account_id=intent.account_id,
            symbol=intent.symbol,
            side=intent.side,
            quantity=intent.quantity,
            status=response.status,
            price=reference_price,
            created_at=datetime.now(tz=UTC),
        )
        self.state.orders[order_id] = order

        self.state.record_event(
            envelope_to_dict(
                build_event_envelope(
                    event_type="order.filled" if response.status == "filled" else "order.submitted",
                    event_version=1,
                    aggregate_type="order",
                    aggregate_id=order_id,
                    strategy_id=intent.strategy_id,
                    deployment_id=intent.deployment_id,
                    account_id=intent.account_id,
                    venue=intent.venue,
                    correlation_id=intent.idempotency_key,
                    payload={"status": response.status},
                )
            )
        )

        self._apply_fill(order)
        return decision

    async def cancel_order(self, order_id: str) -> None:
        response = await self.adapter.cancel_order(order_id)
        if order_id in self.state.orders:
            self.state.orders[order_id].status = response.status

    async def replace_order(self, order_id: str, new_quantity: float, new_price: float) -> None:
        existing = self.state.orders.get(order_id)
        if existing is None:
            return
        response = await self.adapter.replace_order(
            order_id,
            NormalizedOrderRequest(
                account_id=existing.account_id,
                symbol=existing.symbol,
                side=existing.side,
                quantity=new_quantity,
                price=new_price,
            ),
        )
        existing.quantity = new_quantity
        existing.price = new_price
        existing.status = response.status

    def _apply_fill(self, order: OrderView) -> None:
        if order.status != "filled":
            return

        position_key = (order.account_id, order.symbol)
        existing_position = self.state.positions.get(position_key)
        signed_qty = order.quantity if order.side == "buy" else -order.quantity
        if existing_position is None:
            self.state.positions[position_key] = PositionView(
                account_id=order.account_id,
                symbol=order.symbol,
                quantity=signed_qty,
                average_price=order.price,
            )
        else:
            new_qty = existing_position.quantity + signed_qty
            existing_position.quantity = new_qty
            existing_position.average_price = order.price

        balance_key = (order.account_id, "USD")
        existing_balance = self.state.balances.get(balance_key)
        notional = order.quantity * order.price
        delta = -notional if order.side == "buy" else notional
        if existing_balance is None:
            self.state.balances[balance_key] = BalanceView(
                account_id=order.account_id,
                currency="USD",
                total=1_000_000 + delta,
                available=1_000_000 + delta,
            )
        else:
            existing_balance.total += delta
            existing_balance.available += delta
