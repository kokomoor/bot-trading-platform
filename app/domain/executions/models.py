from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class Fill:
    fill_id: UUID
    order_id: UUID
    price: float
    quantity: float
    executed_at: datetime
