from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


async def with_transaction(  # noqa: UP047
    session: AsyncSession,
    operation: Callable[[AsyncSession], Awaitable[T]],
) -> T:
    try:
        result = await operation(session)
        await session.commit()
        return result
    except Exception:
        await session.rollback()
        raise
