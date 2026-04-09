from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.events.envelope import build_event_envelope
from app.infrastructure.repositories import DomainEventRepository, EventQuery


@pytest.mark.integration
@pytest.mark.asyncio
async def test_event_repository_replay_filters(integration_session: AsyncSession) -> None:
    repo = DomainEventRepository(integration_session)
    now = datetime.now(tz=UTC)

    event_1 = build_event_envelope(
        event_type="order.submitted",
        event_version=1,
        aggregate_type="order",
        aggregate_id="order-1",
        correlation_id="corr-1",
        payload={"status": "submitted"},
        account_id="acct-1",
        strategy_id="strat-1",
        metadata={"created_at": now.isoformat()},
    )
    event_2 = build_event_envelope(
        event_type="order.filled",
        event_version=1,
        aggregate_type="order",
        aggregate_id="order-1",
        correlation_id="corr-1",
        payload={"status": "filled"},
        account_id="acct-1",
        strategy_id="strat-1",
        metadata={"created_at": (now + timedelta(seconds=1)).isoformat()},
    )

    await repo.append(event_1)
    await repo.append(event_2)
    await integration_session.commit()

    replayed = await repo.replay(EventQuery(event_type="order.filled", aggregate_id="order-1"))

    assert len(replayed) == 1
    assert replayed[0].event_type == "order.filled"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_outbox_pending_and_mark_published(integration_session: AsyncSession) -> None:
    repo = DomainEventRepository(integration_session)
    event = build_event_envelope(
        event_type="order.intent.created",
        event_version=1,
        aggregate_type="order_intent",
        aggregate_id="intent-1",
        correlation_id="corr-2",
        payload={"side": "buy"},
    )
    await repo.append(event)
    await integration_session.commit()

    pending_before = await repo.pending_outbox()
    assert any(item.event_id == event.event_id for item in pending_before)

    await repo.mark_published(event.event_id)
    await integration_session.commit()

    pending_after = await repo.pending_outbox()
    assert not any(item.event_id == event.event_id for item in pending_after)
