from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.orders.enums import OrderIntentStatus
from app.domain.orders.models import OrderIntent
from app.infrastructure.db.models import OrderIntentModel, OrderIntentStatusDB


class DuplicateIdempotencyKeyError(ValueError):
    """Raised when trying to persist duplicate idempotency key."""


class OrderIntentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, intent: OrderIntent) -> None:
        existing_stmt = select(OrderIntentModel).where(
            OrderIntentModel.idempotency_key == intent.idempotency_key
        )
        existing = await self._session.scalar(existing_stmt)
        if existing is not None:
            raise DuplicateIdempotencyKeyError(intent.idempotency_key)

        row = OrderIntentModel(
            intent_id=str(intent.intent_id),
            strategy_id=str(intent.strategy_id),
            deployment_id=str(intent.deployment_id),
            account_id=str(intent.account_id),
            instrument=intent.instrument,
            side=intent.side,
            quantity=float(intent.quantity),
            idempotency_key=intent.idempotency_key,
            status=OrderIntentStatusDB(intent.status.value),
            reason=None,
            created_at=intent.created_at,
        )
        self._session.add(row)

    async def get_by_idempotency_key(self, idempotency_key: str) -> OrderIntent | None:
        stmt = select(OrderIntentModel).where(OrderIntentModel.idempotency_key == idempotency_key)
        row = await self._session.scalar(stmt)
        if row is None:
            return None
        return OrderIntent(
            intent_id=_uuid_from_str(row.intent_id),
            strategy_id=_uuid_from_str(row.strategy_id),
            deployment_id=_uuid_from_str(row.deployment_id),
            account_id=_uuid_from_str(row.account_id),
            instrument=row.instrument,
            side=row.side,
            quantity=row.quantity,
            idempotency_key=row.idempotency_key,
            status=OrderIntentStatus(row.status.value),
            created_at=row.created_at,
        )


def _uuid_from_str(value: str) -> UUID:
    return UUID(value)
