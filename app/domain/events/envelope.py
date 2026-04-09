from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Any, Protocol

from app.core.ids import new_uuid


class DomainEventPayload(Protocol):
    def to_payload(self) -> dict[str, Any]: ...


@dataclass(frozen=True, slots=True)
class EventEnvelope:
    event_id: str
    event_type: str
    event_version: int
    aggregate_type: str
    aggregate_id: str
    strategy_id: str | None
    deployment_id: str | None
    account_id: str | None
    venue: str | None
    timestamp: datetime
    correlation_id: str
    causation_id: str | None
    payload: dict[str, Any]
    metadata: dict[str, Any]


def build_event_envelope(
    *,
    event_type: str,
    event_version: int,
    aggregate_type: str,
    aggregate_id: str,
    correlation_id: str,
    payload: dict[str, Any],
    strategy_id: str | None = None,
    deployment_id: str | None = None,
    account_id: str | None = None,
    venue: str | None = None,
    causation_id: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> EventEnvelope:
    return EventEnvelope(
        event_id=str(new_uuid()),
        event_type=event_type,
        event_version=event_version,
        aggregate_type=aggregate_type,
        aggregate_id=aggregate_id,
        strategy_id=strategy_id,
        deployment_id=deployment_id,
        account_id=account_id,
        venue=venue,
        timestamp=datetime.now(tz=UTC),
        correlation_id=correlation_id,
        causation_id=causation_id,
        payload=payload,
        metadata=metadata or {},
    )


def envelope_to_dict(envelope: EventEnvelope) -> dict[str, Any]:
    serialized = asdict(envelope)
    serialized["timestamp"] = envelope.timestamp.isoformat()
    return serialized


def envelope_from_dict(data: dict[str, Any]) -> EventEnvelope:
    timestamp_raw = data["timestamp"]
    if isinstance(timestamp_raw, datetime):
        parsed_timestamp = timestamp_raw
    else:
        parsed_timestamp = datetime.fromisoformat(str(timestamp_raw))

    return EventEnvelope(
        event_id=str(data["event_id"]),
        event_type=str(data["event_type"]),
        event_version=int(data["event_version"]),
        aggregate_type=str(data["aggregate_type"]),
        aggregate_id=str(data["aggregate_id"]),
        strategy_id=str(data["strategy_id"]) if data.get("strategy_id") else None,
        deployment_id=str(data["deployment_id"]) if data.get("deployment_id") else None,
        account_id=str(data["account_id"]) if data.get("account_id") else None,
        venue=str(data["venue"]) if data.get("venue") else None,
        timestamp=parsed_timestamp,
        correlation_id=str(data["correlation_id"]),
        causation_id=str(data["causation_id"]) if data.get("causation_id") else None,
        payload=dict(data.get("payload", {})),
        metadata=dict(data.get("metadata", {})),
    )
