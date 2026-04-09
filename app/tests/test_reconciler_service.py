import pytest

from app.infrastructure.adapters.base import (
    FillUpdate,
    NormalizedOrderRequest,
    NormalizedOrderResponse,
)
from app.services.reconciler.service import ReconciliationService
from app.services.shared.platform_state import BalanceView, OrderView, PlatformState, PositionView


class FakeAdapter:
    async def place_order(self, request: NormalizedOrderRequest) -> NormalizedOrderResponse:
        return NormalizedOrderResponse(order_id="x", status="filled")

    async def cancel_order(self, order_id: str) -> NormalizedOrderResponse:
        return NormalizedOrderResponse(order_id=order_id, status="canceled")

    async def replace_order(
        self,
        order_id: str,
        request: NormalizedOrderRequest,
    ) -> NormalizedOrderResponse:
        return NormalizedOrderResponse(order_id=order_id, status="replaced")

    async def get_positions(self, account_id: str) -> list[dict[str, object]]:
        return [{"symbol": "BTC-USD", "quantity": 0.2}]

    async def get_balances(self, account_id: str) -> list[dict[str, object]]:
        return [{"currency": "USD", "total": 900.0}]

    async def get_open_orders(self, account_id: str) -> list[dict[str, object]]:
        return []

    async def stream_order_updates(self) -> list[FillUpdate]:
        return []

    async def healthcheck(self) -> bool:
        return True


@pytest.mark.asyncio
async def test_reconciliation_detects_mismatches() -> None:
    state = PlatformState()
    state.orders["o1"] = OrderView(
        order_id="o1",
        intent_id="i1",
        account_id="acct-1",
        symbol="BTC-USD",
        side="buy",
        quantity=1.0,
        status="submitted",
        price=100.0,
    )
    state.positions[("acct-1", "BTC-USD")] = PositionView(
        account_id="acct-1",
        symbol="BTC-USD",
        quantity=1.0,
        average_price=100.0,
    )
    state.balances[("acct-1", "USD")] = BalanceView(
        account_id="acct-1",
        currency="USD",
        total=1000.0,
        available=1000.0,
    )

    service = ReconciliationService(adapter=FakeAdapter(), state=state)
    issues = await service.reconcile_once("acct-1")

    assert issues
    assert state.reconciliation_issues
    assert any(event["event_type"] == "reconciliation.mismatch_detected" for event in state.events)
