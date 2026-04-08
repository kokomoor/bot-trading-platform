from prometheus_client import CollectorRegistry

from app.core.observability import HealthStatus, build_metrics, render_metrics, summarize_readiness


def test_metrics_registration_and_render() -> None:
    registry = CollectorRegistry(auto_describe=True)
    metrics = build_metrics(registry=registry)

    metrics.http_requests_total.labels(method="GET", path="/health", status="200").inc()
    output = render_metrics(registry)

    assert b"btp_http_requests_total" in output
    assert metrics.registry is registry


def test_readiness_summary() -> None:
    status = summarize_readiness(
        [
            HealthStatus(name="postgres", ok=True),
            HealthStatus(name="redis", ok=False, details={"error": "down"}),
        ]
    )

    assert not status.ok
    assert len(status.checks) == 2
