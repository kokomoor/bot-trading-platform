from datetime import UTC, datetime

from app.core.time import FrozenClock, UtcClock


def test_utc_clock_is_timezone_aware() -> None:
    now = UtcClock().now()
    assert now.tzinfo is not None


def test_frozen_clock_returns_set_time() -> None:
    start = datetime(2026, 1, 1, 0, 0, tzinfo=UTC)
    end = datetime(2026, 1, 1, 1, 0, tzinfo=UTC)

    clock = FrozenClock(current=start)
    assert clock.now() == start

    clock.set(end)
    assert clock.now() == end
