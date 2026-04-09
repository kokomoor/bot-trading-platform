"""Execution engine service."""

from app.core.logging import get_logger

logger = get_logger(service="execution_engine")


def run() -> None:
    logger.info("execution_engine.startup")


if __name__ == "__main__":
    run()
