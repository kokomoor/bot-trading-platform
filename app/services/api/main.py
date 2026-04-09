"""API service entrypoint."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Response
from redis.asyncio import Redis
from sqlalchemy import text

from app.core.config import Settings, get_settings
from app.core.logging import configure_logging, get_logger
from app.core.observability import HealthStatus, build_metrics, render_metrics, summarize_readiness
from app.infrastructure.db import build_engine, build_session_factory
from app.services.shared.platform_state import platform_state
from app.services.shared.runtime import set_kill_switch

logger = get_logger(service="api")


@asynccontextmanager
async def lifespan(api_app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    configure_logging(settings)

    api_app.state.settings = settings
    api_app.state.metrics_registry = None
    if settings.observability.metrics_enabled:
        metrics = build_metrics()
        api_app.state.metrics = metrics
        api_app.state.metrics_registry = metrics.registry

    engine = build_engine(settings)
    session_factory = build_session_factory(engine)
    redis_client = Redis.from_url(
        settings.redis.url,
        socket_timeout=settings.redis.socket_timeout_seconds,
    )

    api_app.state.db_engine = engine
    api_app.state.db_session_factory = session_factory
    api_app.state.redis_client = redis_client

    logger.info("api.startup", env=settings.env.value)
    try:
        yield
    finally:
        await redis_client.aclose()
        await engine.dispose()
        logger.info("api.shutdown")


app = FastAPI(title="bot-trading-platform", version="0.1.0", lifespan=lifespan)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readiness", tags=["system"])
async def readiness() -> dict[str, object]:
    checks: list[HealthStatus] = []

    try:
        async with app.state.db_session_factory() as session:
            await session.execute(text("SELECT 1"))
        checks.append(HealthStatus(name="postgres", ok=True))
    except Exception as exc:
        checks.append(HealthStatus(name="postgres", ok=False, details={"error": str(exc)}))

    try:
        await app.state.redis_client.ping()
        checks.append(HealthStatus(name="redis", ok=True))
    except Exception as exc:
        checks.append(HealthStatus(name="redis", ok=False, details={"error": str(exc)}))

    readiness_status = summarize_readiness(checks)
    return {
        "ok": readiness_status.ok,
        "checks": [
            {"name": check.name, "ok": check.ok, "details": check.details or {}}
            for check in readiness_status.checks
        ],
    }


@app.get("/ready", tags=["system"])
async def ready() -> dict[str, object]:
    return await readiness()


@app.get("/metrics", tags=["system"])
def metrics() -> Response:
    registry = app.state.metrics_registry
    if registry is None:
        return Response(status_code=404, content="metrics disabled")
    return Response(content=render_metrics(registry), media_type="text/plain; version=0.0.4")


@app.get("/admin/strategies", tags=["admin"])
def list_strategies() -> dict[str, object]:
    return {"strategies": platform_state.strategies}


@app.get("/admin/deployments", tags=["admin"])
def list_deployments() -> dict[str, object]:
    return {"deployments": platform_state.deployments}


@app.get("/admin/positions", tags=["admin"])
def list_positions() -> dict[str, object]:
    return {
        "positions": [
            {
                "account_id": position.account_id,
                "symbol": position.symbol,
                "quantity": position.quantity,
                "average_price": position.average_price,
            }
            for position in platform_state.positions.values()
        ]
    }


@app.get("/admin/orders/{order_id}", tags=["admin"])
def order_lookup(order_id: str) -> dict[str, object]:
    order = platform_state.orders.get(order_id)
    if order is None:
        return {"found": False}
    return {
        "found": True,
        "order": {
            "order_id": order.order_id,
            "intent_id": order.intent_id,
            "account_id": order.account_id,
            "symbol": order.symbol,
            "side": order.side,
            "quantity": order.quantity,
            "status": order.status,
            "price": order.price,
        },
    }


@app.get("/admin/events", tags=["admin"])
def event_lookup(limit: int = 100) -> dict[str, object]:
    return {"events": platform_state.events[-limit:]}


@app.get("/admin/kill-switch", tags=["admin"])
def kill_switch_state() -> dict[str, bool]:
    return {"enabled": platform_state.kill_switch_enabled}


@app.post("/admin/kill-switch/{enabled}", tags=["admin"])
def toggle_kill_switch(enabled: bool) -> dict[str, bool]:
    set_kill_switch(enabled)
    return {"enabled": platform_state.kill_switch_enabled}


def run() -> None:
    settings: Settings = get_settings()
    import uvicorn

    uvicorn.run(
        "app.services.api.main:app",
        host=settings.api.host,
        port=settings.api.port,
        reload=False,
        workers=settings.api.workers,
    )


if __name__ == "__main__":
    run()
