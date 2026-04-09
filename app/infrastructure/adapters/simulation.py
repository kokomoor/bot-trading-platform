from __future__ import annotations

from app.core.ids import new_uuid_str
from app.infrastructure.adapters.base import (
    FillUpdate,
    NormalizedOrderRequest,
    NormalizedOrderResponse,
)


class SimulationAdapter:
    def __init__(self) -> None:
        self._orders: dict[str, FillUpdate] = {}

    async def place_order(self, request: NormalizedOrderRequest) -> NormalizedOrderResponse:
        order_id = new_uuid_str()
        fill = FillUpdate(
            order_id=order_id,
            symbol=request.symbol,
            side=request.side,
            quantity=request.quantity,
            price=request.price,
            status="filled",
        )
        self._orders[order_id] = fill
        return NormalizedOrderResponse(order_id=order_id, status="filled")

    async def cancel_order(self, order_id: str) -> NormalizedOrderResponse:
        existing = self._orders.get(order_id)
        if existing:
            self._orders[order_id] = FillUpdate(
                order_id=existing.order_id,
                symbol=existing.symbol,
                side=existing.side,
                quantity=existing.quantity,
                price=existing.price,
                status="canceled",
            )
            return NormalizedOrderResponse(order_id=order_id, status="canceled")
        return NormalizedOrderResponse(order_id=order_id, status="unknown")

    async def replace_order(
        self,
        order_id: str,
        request: NormalizedOrderRequest,
    ) -> NormalizedOrderResponse:
        self._orders[order_id] = FillUpdate(
            order_id=order_id,
            symbol=request.symbol,
            side=request.side,
            quantity=request.quantity,
            price=request.price,
            status="replaced",
        )
        return NormalizedOrderResponse(order_id=order_id, status="replaced")

    async def get_positions(self, account_id: str) -> list[dict[str, object]]:
        return []

    async def get_balances(self, account_id: str) -> list[dict[str, object]]:
        return []

    async def get_open_orders(self, account_id: str) -> list[dict[str, object]]:
        return [
            {
                "order_id": order_id,
                "status": fill.status,
                "symbol": fill.symbol,
                "quantity": fill.quantity,
            }
            for order_id, fill in self._orders.items()
            if fill.status not in {"filled", "canceled"}
        ]

    async def stream_order_updates(self) -> list[FillUpdate]:
        return list(self._orders.values())

    async def healthcheck(self) -> bool:
        return True
