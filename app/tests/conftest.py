from __future__ import annotations

import os
from collections.abc import AsyncIterator

import pytest
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.infrastructure.db import Base


@pytest.fixture(scope="session")
def integration_database_url() -> str:
    return os.getenv("BTP_TEST_DATABASE_URL", "")


@pytest.fixture(scope="session")
async def integration_engine(integration_database_url: str) -> AsyncIterator[AsyncEngine]:
    if not integration_database_url:
        pytest.skip("Set BTP_TEST_DATABASE_URL to run Postgres integration fixtures")

    engine = create_async_engine(integration_database_url, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield engine
    finally:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()


@pytest.fixture()
async def integration_session(integration_engine: AsyncEngine) -> AsyncIterator[AsyncSession]:
    session_factory = async_sessionmaker(
        integration_engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    async with session_factory() as session:
        yield session
        await session.rollback()
