"""Strategy runner placeholder service."""

from app.core.logging import get_logger

logger = get_logger(service="strategy_runner")


def run() -> None:
    logger.info("strategy_runner.startup")


if __name__ == "__main__":
    run()
