from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.core.config import Settings


def build_engine(settings: Settings) -> AsyncEngine:
    return create_async_engine(
        str(settings.database.dsn),
        echo=settings.database.echo,
        pool_pre_ping=True,
        pool_size=settings.database.pool_size,
        max_overflow=settings.database.max_overflow,
        future=True,
    )
