from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from prometheus_client import CollectorRegistry, Counter, Histogram, generate_latest


@dataclass(slots=True)
class TradingMetrics:
    registry: CollectorRegistry
    http_requests_total: Counter
    event_publications_total: Counter
    event_consumption_total: Counter
    order_intents_total: Counter
    risk_decisions_total: Counter
    adapter_errors_total: Counter
    reconciliation_mismatches_total: Counter
    strategy_loop_duration_seconds: Histogram


def build_metrics(registry: CollectorRegistry | None = None) -> TradingMetrics:
    metric_registry = registry or CollectorRegistry(auto_describe=True)

    return TradingMetrics(
        registry=metric_registry,
        http_requests_total=Counter(
            "btp_http_requests_total",
            "Total HTTP requests",
            ["method", "path", "status"],
            registry=metric_registry,
        ),
        event_publications_total=Counter(
            "btp_event_publications_total",
            "Total event publications",
            ["topic", "result"],
            registry=metric_registry,
        ),
        event_consumption_total=Counter(
            "btp_event_consumption_total",
            "Total event consumptions",
            ["topic", "result"],
            registry=metric_registry,
        ),
        order_intents_total=Counter(
            "btp_order_intents_total",
            "Order intent count",
            ["strategy", "instrument"],
            registry=metric_registry,
        ),
        risk_decisions_total=Counter(
            "btp_risk_decisions_total",
            "Risk decisions",
            ["decision", "reason"],
            registry=metric_registry,
        ),
        adapter_errors_total=Counter(
            "btp_adapter_errors_total",
            "Adapter errors",
            ["adapter", "operation", "error_type"],
            registry=metric_registry,
        ),
        reconciliation_mismatches_total=Counter(
            "btp_reconciliation_mismatches_total",
            "Reconciliation mismatches",
            ["mismatch_type"],
            registry=metric_registry,
        ),
        strategy_loop_duration_seconds=Histogram(
            "btp_strategy_loop_duration_seconds",
            "Strategy loop duration",
            ["strategy"],
            registry=metric_registry,
        ),
    )


def render_metrics(registry: CollectorRegistry) -> bytes:
    return cast(bytes, generate_latest(registry))
