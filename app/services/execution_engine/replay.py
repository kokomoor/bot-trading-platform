from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.services.shared.platform_state import PlatformState


@dataclass(frozen=True, slots=True)
class ReplayQuery:
    aggregate_type: str | None = None
    aggregate_id: str | None = None
    strategy_id: str | None = None
    account_id: str | None = None
    from_time: datetime | None = None
    to_time: datetime | None = None
    limit: int = 200


class EventReplayService:
    def __init__(self, state: PlatformState) -> None:
        self._state = state

    def query(self, query: ReplayQuery) -> list[dict[str, object]]:
        filtered: list[dict[str, object]] = []
        for event in self._state.events:
            if query.aggregate_type and event.get("aggregate_type") != query.aggregate_type:
                continue
            if query.aggregate_id and event.get("aggregate_id") != query.aggregate_id:
                continue
            if query.strategy_id and event.get("strategy_id") != query.strategy_id:
                continue
            if query.account_id and event.get("account_id") != query.account_id:
                continue

            timestamp_raw = event.get("timestamp")
            if isinstance(timestamp_raw, str):
                ts = datetime.fromisoformat(timestamp_raw)
            elif isinstance(timestamp_raw, datetime):
                ts = timestamp_raw
            else:
                filtered.append(event)
                continue

            if query.from_time and ts < query.from_time:
                continue
            if query.to_time and ts > query.to_time:
                continue
            filtered.append(event)

        return filtered[-query.limit :]

    def replay(self, query: ReplayQuery, *, recovery_mode: bool = False) -> list[dict[str, object]]:
        results = self.query(query)
        if not recovery_mode:
            return results

        for event in results:
            event.setdefault("metadata", {})
            metadata = event["metadata"]
            if isinstance(metadata, dict):
                metadata["replayed_in_recovery_mode"] = True
        return results
