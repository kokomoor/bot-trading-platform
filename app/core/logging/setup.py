from __future__ import annotations

import contextvars
import logging
import sys

import structlog

from app.core.config import Settings
from app.core.ids import new_correlation_id

correlation_id_ctx: contextvars.ContextVar[str] = contextvars.ContextVar(
    "correlation_id",
    default="",
)


def get_correlation_id() -> str:
    correlation_id = correlation_id_ctx.get()
    if not correlation_id:
        correlation_id = new_correlation_id()
        correlation_id_ctx.set(correlation_id)
    return correlation_id


def bind_correlation_id(correlation_id: str | None = None) -> str:
    value = correlation_id or new_correlation_id()
    correlation_id_ctx.set(value)
    structlog.contextvars.bind_contextvars(correlation_id=value)
    return value


def clear_correlation_id() -> None:
    correlation_id_ctx.set("")
    structlog.contextvars.clear_contextvars()


def configure_logging(settings: Settings) -> None:
    renderer: structlog.types.Processor
    if settings.is_prod:
        renderer = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer()

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.observability.log_level.upper(), logging.INFO),
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            renderer,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_logger(**bind_values: object) -> structlog.stdlib.BoundLogger:
    logger = structlog.get_logger()
    if bind_values:
        logger = logger.bind(**bind_values)
    return logger
