"""CLI placeholder entrypoint."""

import argparse
import asyncio

from app.core.logging import get_logger
from app.services.shared.platform_state import platform_state
from app.services.simulation.main import run as run_simulation
from app.services.strategy_runner.main import run_once as run_strategy_once

logger = get_logger(interface="cli")


def _seed_demo_data() -> None:
    platform_state.deployments["deploy_ma_cross"] = {
        "strategy_id": "ma_cross",
        "account_id": "paper-account-1",
    }
    platform_state.deployments["deploy_threshold_reversion"] = {
        "strategy_id": "threshold_reversion",
        "account_id": "paper-account-1",
    }
    logger.info("cli.seed_demo_data", deployments=len(platform_state.deployments))


def _inspect_events(limit: int) -> None:
    for event in platform_state.events[-limit:]:
        logger.info("cli.event", **event)


def main() -> None:
    parser = argparse.ArgumentParser(prog="btp")
    parser.add_argument(
        "command",
        choices=["seed-demo-data", "run-simulation", "run-strategy-once", "inspect-events"],
    )
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    if args.command == "seed-demo-data":
        _seed_demo_data()
        return
    if args.command == "run-simulation":
        run_simulation()
        return
    if args.command == "run-strategy-once":
        asyncio.run(run_strategy_once())
        return
    if args.command == "inspect-events":
        _inspect_events(args.limit)
        return


if __name__ == "__main__":
    main()
