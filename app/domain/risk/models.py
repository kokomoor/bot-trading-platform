from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class RiskDecision:
    decision_id: UUID
    intent_id: UUID
    approved: bool
    reason: str
