from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(slots=True)
class PositionView:
    account_id: str
    symbol: str
    quantity: float
    average_price: float


@dataclass(slots=True)
class BalanceView:
    account_id: str
    currency: str
    total: float
    available: float


@dataclass(slots=True)
class OrderView:
    order_id: str
    intent_id: str
    account_id: str
    symbol: str
    side: str
    quantity: float
    status: str
    price: float
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))


@dataclass(slots=True)
class PlatformState:
    kill_switch_enabled: bool = False
    strategies: dict[str, dict[str, str]] = field(default_factory=dict)
    deployments: dict[str, dict[str, str]] = field(default_factory=dict)
    positions: dict[tuple[str, str], PositionView] = field(default_factory=dict)
    balances: dict[tuple[str, str], BalanceView] = field(default_factory=dict)
    orders: dict[str, OrderView] = field(default_factory=dict)
    events: list[dict[str, object]] = field(default_factory=list)

    def record_event(self, event: dict[str, object]) -> None:
        self.events.append(event)


platform_state = PlatformState()
