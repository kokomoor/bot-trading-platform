from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class Position:
    position_id: UUID
    account_id: UUID
    instrument: str
    quantity: float
    updated_at: datetime
