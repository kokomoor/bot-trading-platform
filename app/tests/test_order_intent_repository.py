from datetime import UTC, datetime
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.orders.enums import OrderIntentStatus
from app.domain.orders.models import OrderIntent
from app.infrastructure.db.models import (
    AccountModel,
    StrategyDeploymentModel,
    StrategyDeploymentStatus,
    StrategyModel,
)
from app.infrastructure.repositories import DuplicateIdempotencyKeyError, OrderIntentRepository


@pytest.mark.integration
@pytest.mark.asyncio
async def test_order_intent_idempotency_enforced(integration_session: AsyncSession) -> None:
    repo = OrderIntentRepository(integration_session)
    key = "idem-dup-1"
    strategy_id = uuid4()
    account_id = uuid4()
    deployment_id = uuid4()
    integration_session.add(
        AccountModel(
            account_id=str(account_id),
            venue="sim",
            external_account_ref="acct-ref",
            is_active=True,
            created_at=datetime.now(tz=UTC),
        )
    )
    integration_session.add(
        StrategyModel(
            strategy_id=str(strategy_id),
            code="demo_strategy",
            name="Demo Strategy",
            enabled=True,
            config={},
            created_at=datetime.now(tz=UTC),
        )
    )
    integration_session.add(
        StrategyDeploymentModel(
            deployment_id=str(deployment_id),
            strategy_id=str(strategy_id),
            account_id=str(account_id),
            status=StrategyDeploymentStatus.RUNNING,
            started_at=datetime.now(tz=UTC),
        )
    )
    await integration_session.commit()

    intent = OrderIntent(
        intent_id=uuid4(),
        strategy_id=strategy_id,
        deployment_id=deployment_id,
        account_id=account_id,
        instrument="BTC-USD",
        side="buy",
        quantity=1.0,
        idempotency_key=key,
        status=OrderIntentStatus.CREATED,
        created_at=datetime.now(tz=UTC),
    )

    await repo.create(intent)
    await integration_session.commit()

    duplicate = OrderIntent(
        intent_id=uuid4(),
        strategy_id=strategy_id,
        deployment_id=deployment_id,
        account_id=account_id,
        instrument="BTC-USD",
        side="buy",
        quantity=1.0,
        idempotency_key=key,
        status=OrderIntentStatus.CREATED,
        created_at=datetime.now(tz=UTC),
    )

    with pytest.raises(DuplicateIdempotencyKeyError):
        await repo.create(duplicate)
