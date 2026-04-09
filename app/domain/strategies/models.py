from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class Strategy:
    strategy_id: UUID
    code: str
    name: str
    enabled: bool = True
