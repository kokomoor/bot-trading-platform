from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class MarketTick:
    symbol: str
    price: float
    timestamp: datetime
