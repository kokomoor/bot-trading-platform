from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

from sqlalchemy import (
    JSON,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base import Base


class StrategyDeploymentStatus(StrEnum):
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"


class OrderIntentStatusDB(StrEnum):
    CREATED = "created"
    RISK_APPROVED = "risk_approved"
    RISK_REJECTED = "risk_rejected"


class OrderStatusDB(StrEnum):
    PENDING_SUBMIT = "pending_submit"
    SUBMITTED = "submitted"
    ACKNOWLEDGED = "acknowledged"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELED = "canceled"
    REJECTED = "rejected"


class AccountModel(Base):
    __tablename__ = "accounts"

    account_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    venue: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    external_account_ref: Mapped[str] = mapped_column(String(128), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        UniqueConstraint("venue", "external_account_ref", name="uq_account_venue_ref"),
    )


class StrategyModel(Base):
    __tablename__ = "strategies"

    strategy_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    code: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    enabled: Mapped[bool] = mapped_column(default=True, nullable=False)
    config: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class StrategyDeploymentModel(Base):
    __tablename__ = "strategy_deployments"

    deployment_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    strategy_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("strategies.strategy_id", ondelete="CASCADE"),
        nullable=False,
    )
    account_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("accounts.account_id", ondelete="CASCADE"),
        nullable=False,
    )
    status: Mapped[StrategyDeploymentStatus] = mapped_column(
        Enum(StrategyDeploymentStatus, native_enum=False),
        nullable=False,
    )
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        Index("ix_deployments_strategy_status", "strategy_id", "status"),
        UniqueConstraint("strategy_id", "account_id", "status", name="uq_deployment_unique_status"),
    )


class OrderIntentModel(Base):
    __tablename__ = "order_intents"

    intent_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    strategy_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("strategies.strategy_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    deployment_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("strategy_deployments.deployment_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    account_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("accounts.account_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    instrument: Mapped[str] = mapped_column(String(64), nullable=False)
    side: Mapped[str] = mapped_column(String(8), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    status: Mapped[OrderIntentStatusDB] = mapped_column(
        Enum(OrderIntentStatusDB, native_enum=False),
        nullable=False,
    )
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )


class OrderModel(Base):
    __tablename__ = "orders"

    order_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    intent_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("order_intents.intent_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    account_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("accounts.account_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    venue_order_id: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    status: Mapped[OrderStatusDB] = mapped_column(
        Enum(OrderStatusDB, native_enum=False),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (Index("ix_orders_account_status", "account_id", "status"),)


class FillModel(Base):
    __tablename__ = "fills"

    fill_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    order_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("orders.order_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    trade_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    fee: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    executed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class PositionModel(Base):
    __tablename__ = "positions"

    position_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    account_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("accounts.account_id", ondelete="CASCADE"),
        nullable=False,
    )
    instrument: Mapped[str] = mapped_column(String(64), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    average_price: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        UniqueConstraint("account_id", "instrument", name="uq_positions_account_instrument"),
        Index("ix_positions_account_instrument", "account_id", "instrument"),
    )


class BalanceSnapshotModel(Base):
    __tablename__ = "balance_snapshots"

    snapshot_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    account_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("accounts.account_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    currency: Mapped[str] = mapped_column(String(16), nullable=False)
    total: Mapped[float] = mapped_column(Float, nullable=False)
    available: Mapped[float] = mapped_column(Float, nullable=False)
    captured_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )


class DomainEventModel(Base):
    __tablename__ = "domain_events"

    event_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    event_type: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    event_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    aggregate_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    aggregate_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    strategy_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    deployment_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    account_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    venue: Mapped[str | None] = mapped_column(String(64), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    correlation_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    causation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    metadata: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    published: Mapped[bool] = mapped_column(default=False, nullable=False, index=True)

    __table_args__ = (
        Index("ix_events_type_time", "event_type", "timestamp"),
        Index("ix_events_aggregate_time", "aggregate_type", "aggregate_id", "timestamp"),
    )


class ReconciliationIssueModel(Base):
    __tablename__ = "reconciliation_issues"

    issue_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    account_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("accounts.account_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    issue_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    severity: Mapped[str] = mapped_column(String(32), nullable=False)
    details: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


__all__ = [
    "AccountModel",
    "BalanceSnapshotModel",
    "DomainEventModel",
    "FillModel",
    "OrderIntentModel",
    "OrderModel",
    "PositionModel",
    "ReconciliationIssueModel",
    "StrategyDeploymentModel",
    "StrategyModel",
]
