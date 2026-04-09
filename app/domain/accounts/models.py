from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class Account:
    account_id: UUID
    venue: str
    external_account_ref: str
    is_active: bool = True
