from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from app.domain.market_data import MarketTick


@dataclass(slots=True)
class SimulatedMarketFeed:
    symbol: str
    seed_price: float
    step: float = 1.0
    length: int = 50

    def stream(self) -> Iterator[MarketTick]:
        now = datetime.now(tz=UTC)
        price = self.seed_price
        direction = 1.0
        for index in range(self.length):
            if index % 5 == 0:
                direction *= -1
            price += direction * self.step
            yield MarketTick(
                symbol=self.symbol,
                price=round(price, 2),
                timestamp=now + timedelta(seconds=index),
            )
