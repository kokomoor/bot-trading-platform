from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class HealthStatus:
    name: str
    ok: bool
    details: dict[str, str] | None = None


@dataclass(frozen=True, slots=True)
class ReadinessStatus:
    ok: bool
    checks: tuple[HealthStatus, ...]


def summarize_readiness(checks: list[HealthStatus]) -> ReadinessStatus:
    return ReadinessStatus(ok=all(check.ok for check in checks), checks=tuple(checks))
