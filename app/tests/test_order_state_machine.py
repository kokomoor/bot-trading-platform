import pytest

from app.domain.orders.enums import OrderStatus
from app.domain.orders.state_machine import InvalidOrderTransitionError, OrderStateMachine


def test_order_state_machine_valid_transitions() -> None:
    machine = OrderStateMachine(current_status=OrderStatus.PENDING_SUBMIT)
    machine = machine.transition(OrderStatus.SUBMITTED)
    machine = machine.transition(OrderStatus.ACKNOWLEDGED)
    machine = machine.transition(OrderStatus.PARTIALLY_FILLED)
    machine = machine.transition(OrderStatus.FILLED)

    assert machine.current_status is OrderStatus.FILLED


def test_order_state_machine_invalid_transition() -> None:
    machine = OrderStateMachine(current_status=OrderStatus.PENDING_SUBMIT)

    with pytest.raises(InvalidOrderTransitionError):
        machine.transition(OrderStatus.FILLED)
