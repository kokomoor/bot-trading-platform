from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class ReconciliationIssue:
    issue_id: UUID
    account_id: UUID
    issue_type: str
    severity: str
    details: dict[str, str]
    detected_at: datetime
