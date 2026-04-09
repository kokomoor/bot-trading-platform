from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class NormalizedOrderRequest:
    account_id: str
    symbol: str
    side: str
    quantity: float
    price: float


@dataclass(frozen=True, slots=True)
class NormalizedOrderResponse:
    order_id: str
    status: str


@dataclass(frozen=True, slots=True)
class FillUpdate:
    order_id: str
    symbol: str
    side: str
    quantity: float
    price: float
    status: str


class TradingAdapter(Protocol):
    async def place_order(self, request: NormalizedOrderRequest) -> NormalizedOrderResponse: ...

    async def cancel_order(self, order_id: str) -> NormalizedOrderResponse: ...

    async def replace_order(
        self,
        order_id: str,
        request: NormalizedOrderRequest,
    ) -> NormalizedOrderResponse: ...

    async def get_positions(self, account_id: str) -> list[dict[str, object]]: ...

    async def get_balances(self, account_id: str) -> list[dict[str, object]]: ...

    async def get_open_orders(self, account_id: str) -> list[dict[str, object]]: ...

    async def stream_order_updates(self) -> list[FillUpdate]: ...

    async def healthcheck(self) -> bool: ...
