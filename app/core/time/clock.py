from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Protocol


class Clock(Protocol):
    def now(self) -> datetime: ...


@dataclass(slots=True)
class UtcClock:
    def now(self) -> datetime:
        return datetime.now(tz=UTC)


@dataclass(slots=True)
class FrozenClock:
    current: datetime

    def now(self) -> datetime:
        return self.current

    def set(self, new_value: datetime) -> None:
        self.current = new_value
