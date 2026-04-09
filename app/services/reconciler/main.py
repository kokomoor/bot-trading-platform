"""Reconciler placeholder service."""

from app.core.logging import get_logger

logger = get_logger(service="reconciler")


def run() -> None:
    logger.info("reconciler.startup")


if __name__ == "__main__":
    run()
