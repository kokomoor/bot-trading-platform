from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class BalanceSnapshot:
    snapshot_id: UUID
    account_id: UUID
    currency: str
    total: float
    available: float
    captured_at: datetime
