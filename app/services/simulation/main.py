"""Simulation service."""

from app.core.logging import get_logger

logger = get_logger(service="simulation")


def run() -> None:
    logger.info("simulation.startup")


if __name__ == "__main__":
    run()
