from app.domain.events.envelope import (
    build_event_envelope,
    envelope_from_dict,
    envelope_to_dict,
)


def test_event_envelope_creation_and_round_trip() -> None:
    envelope = build_event_envelope(
        event_type="order.intent.created",
        event_version=1,
        aggregate_type="order_intent",
        aggregate_id="intent-123",
        correlation_id="corr-123",
        payload={"side": "buy", "quantity": 1.2},
        strategy_id="strategy-1",
        account_id="account-1",
    )

    assert envelope.event_type == "order.intent.created"
    assert envelope.event_id

    serialized = envelope_to_dict(envelope)
    restored = envelope_from_dict(serialized)

    assert restored == envelope
