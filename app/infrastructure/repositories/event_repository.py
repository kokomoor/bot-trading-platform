from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from sqlalchemy import Select, and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.events.envelope import EventEnvelope, envelope_from_dict, envelope_to_dict
from app.infrastructure.db.models import DomainEventModel


@dataclass(slots=True)
class EventQuery:
    event_type: str | None = None
    aggregate_type: str | None = None
    aggregate_id: str | None = None
    strategy_id: str | None = None
    account_id: str | None = None
    from_time: datetime | None = None
    to_time: datetime | None = None
    limit: int = 100


class DomainEventRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def append(self, envelope: EventEnvelope) -> None:
        event_dict = envelope_to_dict(envelope)
        row = DomainEventModel(**event_dict, published=False)
        self._session.add(row)

    async def mark_published(self, event_id: str) -> None:
        row = await self._session.get(DomainEventModel, event_id)
        if row is None:
            return
        row.published = True

    async def pending_outbox(self, *, limit: int = 100) -> list[EventEnvelope]:
        stmt = (
            select(DomainEventModel)
            .where(DomainEventModel.published.is_(False))
            .order_by(DomainEventModel.timestamp.asc())
            .limit(limit)
        )
        rows = (await self._session.scalars(stmt)).all()
        return [self._to_envelope(row) for row in rows]

    async def replay(self, query: EventQuery) -> list[EventEnvelope]:
        stmt: Select[tuple[DomainEventModel]] = select(DomainEventModel)
        filters: list[Any] = []
        if query.event_type:
            filters.append(DomainEventModel.event_type == query.event_type)
        if query.aggregate_type:
            filters.append(DomainEventModel.aggregate_type == query.aggregate_type)
        if query.aggregate_id:
            filters.append(DomainEventModel.aggregate_id == query.aggregate_id)
        if query.strategy_id:
            filters.append(DomainEventModel.strategy_id == query.strategy_id)
        if query.account_id:
            filters.append(DomainEventModel.account_id == query.account_id)
        if query.from_time:
            filters.append(DomainEventModel.timestamp >= query.from_time)
        if query.to_time:
            filters.append(DomainEventModel.timestamp <= query.to_time)

        if filters:
            stmt = stmt.where(and_(*filters))

        stmt = stmt.order_by(DomainEventModel.timestamp.asc()).limit(query.limit)
        rows = (await self._session.scalars(stmt)).all()
        return [self._to_envelope(row) for row in rows]

    @staticmethod
    def _to_envelope(row: DomainEventModel) -> EventEnvelope:
        return envelope_from_dict(
            {
                "event_id": row.event_id,
                "event_type": row.event_type,
                "event_version": row.event_version,
                "aggregate_type": row.aggregate_type,
                "aggregate_id": row.aggregate_id,
                "strategy_id": row.strategy_id,
                "deployment_id": row.deployment_id,
                "account_id": row.account_id,
                "venue": row.venue,
                "timestamp": row.timestamp,
                "correlation_id": row.correlation_id,
                "causation_id": row.causation_id,
                "payload": row.payload,
                "metadata": row.metadata,
            }
        )
