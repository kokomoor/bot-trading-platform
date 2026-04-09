"""Reconciler placeholder service."""

import asyncio

from app.core.logging import get_logger
from app.services.reconciler.service import ReconciliationService
from app.services.shared.platform_state import platform_state
from app.services.shared.runtime import execution_engine

logger = get_logger(service="reconciler")


async def run_once(account_id: str = "paper-account-1") -> None:
    service = ReconciliationService(adapter=execution_engine.adapter, state=platform_state)
    issues = await service.reconcile_once(account_id=account_id)
    logger.info("reconciler.completed", account_id=account_id, issue_count=len(issues))


def run() -> None:
    logger.info("reconciler.startup")
    asyncio.run(run_once())


if __name__ == "__main__":
    run()
