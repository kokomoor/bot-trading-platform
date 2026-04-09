from __future__ import annotations

from dataclasses import dataclass

from app.domain.orders.enums import OrderStatus

_ALLOWED_TRANSITIONS: dict[OrderStatus, set[OrderStatus]] = {
    OrderStatus.PENDING_SUBMIT: {OrderStatus.SUBMITTED, OrderStatus.REJECTED},
    OrderStatus.SUBMITTED: {OrderStatus.ACKNOWLEDGED, OrderStatus.REJECTED, OrderStatus.CANCELED},
    OrderStatus.ACKNOWLEDGED: {
        OrderStatus.PARTIALLY_FILLED,
        OrderStatus.FILLED,
        OrderStatus.CANCELED,
        OrderStatus.REJECTED,
    },
    OrderStatus.PARTIALLY_FILLED: {
        OrderStatus.PARTIALLY_FILLED,
        OrderStatus.FILLED,
        OrderStatus.CANCELED,
    },
    OrderStatus.FILLED: set(),
    OrderStatus.CANCELED: set(),
    OrderStatus.REJECTED: set(),
}


class InvalidOrderTransitionError(ValueError):
    """Raised when invalid order state transition is attempted."""


@dataclass(frozen=True, slots=True)
class OrderStateMachine:
    current_status: OrderStatus

    def can_transition(self, next_status: OrderStatus) -> bool:
        return next_status in _ALLOWED_TRANSITIONS[self.current_status]

    def transition(self, next_status: OrderStatus) -> OrderStateMachine:
        if not self.can_transition(next_status):
            raise InvalidOrderTransitionError(
                f"cannot transition from {self.current_status.value} to {next_status.value}"
            )
        return OrderStateMachine(current_status=next_status)
