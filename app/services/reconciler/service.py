from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.domain.events.envelope import build_event_envelope, envelope_to_dict
from app.infrastructure.adapters.base import TradingAdapter
from app.services.shared.platform_state import PlatformState


@dataclass(frozen=True, slots=True)
class ReconciliationIssue:
    issue_id: str
    issue_type: str
    severity: str
    account_id: str
    details: dict[str, object]
    detected_at: datetime


@dataclass(slots=True)
class ReconciliationService:
    adapter: TradingAdapter
    state: PlatformState
    _lock: asyncio.Lock = field(default_factory=asyncio.Lock)

    async def reconcile_once(self, account_id: str) -> list[ReconciliationIssue]:
        async with self._lock:
            issues: list[ReconciliationIssue] = []

            adapter_orders = await self.adapter.get_open_orders(account_id)
            adapter_positions = await self.adapter.get_positions(account_id)
            adapter_balances = await self.adapter.get_balances(account_id)

            issues.extend(self._reconcile_orders(account_id, adapter_orders))
            issues.extend(self._reconcile_positions(account_id, adapter_positions))
            issues.extend(self._reconcile_balances(account_id, adapter_balances))

            for issue in issues:
                issue_dict = {
                    "issue_id": issue.issue_id,
                    "issue_type": issue.issue_type,
                    "severity": issue.severity,
                    "account_id": issue.account_id,
                    "details": issue.details,
                    "detected_at": issue.detected_at.isoformat(),
                }
                self.state.reconciliation_issues.append(issue_dict)
                self.state.record_event(
                    envelope_to_dict(
                        build_event_envelope(
                            event_type="reconciliation.mismatch_detected",
                            event_version=1,
                            aggregate_type="account",
                            aggregate_id=account_id,
                            account_id=account_id,
                            correlation_id=issue.issue_id,
                            payload=issue_dict,
                        )
                    )
                )

            return issues

    def _reconcile_orders(
        self,
        account_id: str,
        adapter_orders: list[dict[str, object]],
    ) -> list[ReconciliationIssue]:
        internal_open = {
            order_id: order
            for order_id, order in self.state.orders.items()
            if order.account_id == account_id
            and order.status not in {"filled", "canceled", "rejected"}
        }
        adapter_open_ids = {str(order.get("order_id")) for order in adapter_orders}

        issues: list[ReconciliationIssue] = []
        for internal_order_id in internal_open:
            if internal_order_id not in adapter_open_ids:
                issues.append(
                    self._issue(
                        issue_type="order_missing_on_adapter",
                        severity="high",
                        account_id=account_id,
                        details={"order_id": internal_order_id},
                    )
                )
        return issues

    def _reconcile_positions(
        self,
        account_id: str,
        adapter_positions: list[dict[str, object]],
    ) -> list[ReconciliationIssue]:
        adapter_map = {
            str(item.get("symbol")): float(item.get("quantity", 0))
            for item in adapter_positions
        }
        issues: list[ReconciliationIssue] = []
        for (acct, symbol), position in self.state.positions.items():
            if acct != account_id:
                continue
            adapter_qty = adapter_map.get(symbol)
            if adapter_qty is None:
                issues.append(
                    self._issue(
                        issue_type="position_missing_on_adapter",
                        severity="medium",
                        account_id=account_id,
                        details={"symbol": symbol, "internal_qty": position.quantity},
                    )
                )
            elif abs(adapter_qty - position.quantity) > 1e-9:
                issues.append(
                    self._issue(
                        issue_type="position_quantity_mismatch",
                        severity="high",
                        account_id=account_id,
                        details={
                            "symbol": symbol,
                            "internal_qty": position.quantity,
                            "adapter_qty": adapter_qty,
                        },
                    )
                )
        return issues

    def _reconcile_balances(
        self,
        account_id: str,
        adapter_balances: list[dict[str, object]],
    ) -> list[ReconciliationIssue]:
        adapter_map = {
            (str(item.get("currency")), "total"): float(item.get("total", 0))
            for item in adapter_balances
        }
        issues: list[ReconciliationIssue] = []
        for (acct, currency), balance in self.state.balances.items():
            if acct != account_id:
                continue
            adapter_total = adapter_map.get((currency, "total"))
            if adapter_total is None:
                issues.append(
                    self._issue(
                        issue_type="balance_missing_on_adapter",
                        severity="medium",
                        account_id=account_id,
                        details={"currency": currency, "internal_total": balance.total},
                    )
                )
            elif abs(adapter_total - balance.total) > 1e-9:
                issues.append(
                    self._issue(
                        issue_type="balance_total_mismatch",
                        severity="high",
                        account_id=account_id,
                        details={
                            "currency": currency,
                            "internal_total": balance.total,
                            "adapter_total": adapter_total,
                        },
                    )
                )
        return issues

    @staticmethod
    def _issue(
        *,
        issue_type: str,
        severity: str,
        account_id: str,
        details: dict[str, object],
    ) -> ReconciliationIssue:
        ts = datetime.now(tz=UTC)
        issue_id = f"rec-{int(ts.timestamp() * 1_000_000)}-{issue_type}"
        return ReconciliationIssue(
            issue_id=issue_id,
            issue_type=issue_type,
            severity=severity,
            account_id=account_id,
            details=details,
            detected_at=ts,
        )
