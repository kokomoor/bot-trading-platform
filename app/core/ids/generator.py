from __future__ import annotations

from uuid import UUID, uuid4


def new_uuid() -> UUID:
    return uuid4()


def new_uuid_str() -> str:
    return str(new_uuid())


def new_correlation_id() -> str:
    return f"corr_{new_uuid_str()}"


def new_idempotency_key(prefix: str = "idem") -> str:
    return f"{prefix}_{new_uuid_str()}"
