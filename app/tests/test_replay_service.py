from datetime import UTC, datetime, timedelta

from app.services.execution_engine.replay import EventReplayService, ReplayQuery
from app.services.shared.platform_state import PlatformState


def test_replay_query_filters_and_recovery_marker() -> None:
    state = PlatformState()
    now = datetime.now(tz=UTC)
    state.events = [
        {
            "event_type": "order.submitted",
            "aggregate_type": "order",
            "aggregate_id": "o1",
            "strategy_id": "s1",
            "account_id": "a1",
            "timestamp": now.isoformat(),
            "metadata": {},
        },
        {
            "event_type": "order.filled",
            "aggregate_type": "order",
            "aggregate_id": "o1",
            "strategy_id": "s1",
            "account_id": "a1",
            "timestamp": (now + timedelta(seconds=1)).isoformat(),
            "metadata": {},
        },
    ]

    replay = EventReplayService(state)
    results = replay.query(ReplayQuery(aggregate_type="order", aggregate_id="o1", limit=10))
    assert len(results) == 2

    recovery_results = replay.replay(ReplayQuery(limit=10), recovery_mode=True)
    assert recovery_results[0]["metadata"]["replayed_in_recovery_mode"] is True
