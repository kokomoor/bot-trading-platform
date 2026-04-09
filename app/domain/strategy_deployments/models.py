from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class StrategyDeployment:
    deployment_id: UUID
    strategy_id: UUID
    account_id: UUID
    started_at: datetime
    status: str
