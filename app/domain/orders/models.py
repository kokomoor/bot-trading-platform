from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.orders.enums import OrderIntentStatus, OrderStatus


@dataclass(frozen=True, slots=True)
class OrderIntent:
    intent_id: UUID
    strategy_id: UUID
    deployment_id: UUID
    account_id: UUID
    instrument: str
    side: str
    quantity: float
    idempotency_key: str
    status: OrderIntentStatus
    created_at: datetime


@dataclass(frozen=True, slots=True)
class Order:
    order_id: UUID
    intent_id: UUID
    account_id: UUID
    venue_order_id: str | None
    status: OrderStatus
    created_at: datetime
