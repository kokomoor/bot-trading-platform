"""create domain and event backbone tables

Revision ID: 20260409_0001
Revises:
Create Date: 2026-04-09 00:00:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "20260409_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "accounts",
        sa.Column("account_id", sa.String(length=36), nullable=False),
        sa.Column("venue", sa.String(length=64), nullable=False),
        sa.Column("external_account_ref", sa.String(length=128), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("account_id", name=op.f("pk_accounts")),
        sa.UniqueConstraint("venue", "external_account_ref", name="uq_account_venue_ref"),
    )
    op.create_index(op.f("ix_accounts_venue"), "accounts", ["venue"], unique=False)

    op.create_table(
        "strategies",
        sa.Column("strategy_id", sa.String(length=36), nullable=False),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.Column("config", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("strategy_id", name=op.f("pk_strategies")),
        sa.UniqueConstraint("code", name=op.f("uq_strategies_code")),
    )

    deployment_status = sa.Enum("running", "paused", "stopped", name="strategydeploymentstatus")
    order_intent_status = sa.Enum(
        "created", "risk_approved", "risk_rejected", name="orderintentstatusdb"
    )
    order_status = sa.Enum(
        "pending_submit",
        "submitted",
        "acknowledged",
        "partially_filled",
        "filled",
        "canceled",
        "rejected",
        name="orderstatusdb",
    )
    deployment_status.create(op.get_bind())
    order_intent_status.create(op.get_bind())
    order_status.create(op.get_bind())

    op.create_table(
        "strategy_deployments",
        sa.Column("deployment_id", sa.String(length=36), nullable=False),
        sa.Column("strategy_id", sa.String(length=36), nullable=False),
        sa.Column("account_id", sa.String(length=36), nullable=False),
        sa.Column("status", deployment_status, nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["account_id"], ["accounts.account_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["strategy_id"], ["strategies.strategy_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("deployment_id", name=op.f("pk_strategy_deployments")),
        sa.UniqueConstraint(
            "strategy_id",
            "account_id",
            "status",
            name="uq_deployment_unique_status",
        ),
    )
    op.create_index(
        "ix_deployments_strategy_status",
        "strategy_deployments",
        ["strategy_id", "status"],
        unique=False,
    )

    op.create_table(
        "order_intents",
        sa.Column("intent_id", sa.String(length=36), nullable=False),
        sa.Column("strategy_id", sa.String(length=36), nullable=False),
        sa.Column("deployment_id", sa.String(length=36), nullable=False),
        sa.Column("account_id", sa.String(length=36), nullable=False),
        sa.Column("instrument", sa.String(length=64), nullable=False),
        sa.Column("side", sa.String(length=8), nullable=False),
        sa.Column("quantity", sa.Float(), nullable=False),
        sa.Column("idempotency_key", sa.String(length=128), nullable=False),
        sa.Column("status", order_intent_status, nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["account_id"], ["accounts.account_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["deployment_id"],
            ["strategy_deployments.deployment_id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(["strategy_id"], ["strategies.strategy_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("intent_id", name=op.f("pk_order_intents")),
        sa.UniqueConstraint("idempotency_key", name=op.f("uq_order_intents_idempotency_key")),
    )
    op.create_index(op.f("ix_order_intents_account_id"), "order_intents", ["account_id"], unique=False)
    op.create_index(op.f("ix_order_intents_created_at"), "order_intents", ["created_at"], unique=False)
    op.create_index(op.f("ix_order_intents_deployment_id"), "order_intents", ["deployment_id"], unique=False)
    op.create_index(op.f("ix_order_intents_strategy_id"), "order_intents", ["strategy_id"], unique=False)

    op.create_table(
        "orders",
        sa.Column("order_id", sa.String(length=36), nullable=False),
        sa.Column("intent_id", sa.String(length=36), nullable=False),
        sa.Column("account_id", sa.String(length=36), nullable=False),
        sa.Column("venue_order_id", sa.String(length=128), nullable=True),
        sa.Column("status", order_status, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["account_id"], ["accounts.account_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["intent_id"], ["order_intents.intent_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("order_id", name=op.f("pk_orders")),
    )
    op.create_index(op.f("ix_orders_account_id"), "orders", ["account_id"], unique=False)
    op.create_index(op.f("ix_orders_intent_id"), "orders", ["intent_id"], unique=False)
    op.create_index(op.f("ix_orders_venue_order_id"), "orders", ["venue_order_id"], unique=False)
    op.create_index("ix_orders_account_status", "orders", ["account_id", "status"], unique=False)

    op.create_table(
        "fills",
        sa.Column("fill_id", sa.String(length=36), nullable=False),
        sa.Column("order_id", sa.String(length=36), nullable=False),
        sa.Column("trade_id", sa.String(length=128), nullable=True),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("quantity", sa.Float(), nullable=False),
        sa.Column("fee", sa.Float(), nullable=False),
        sa.Column("executed_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["order_id"], ["orders.order_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("fill_id", name=op.f("pk_fills")),
    )
    op.create_index(op.f("ix_fills_order_id"), "fills", ["order_id"], unique=False)

    op.create_table(
        "positions",
        sa.Column("position_id", sa.String(length=36), nullable=False),
        sa.Column("account_id", sa.String(length=36), nullable=False),
        sa.Column("instrument", sa.String(length=64), nullable=False),
        sa.Column("quantity", sa.Float(), nullable=False),
        sa.Column("average_price", sa.Float(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["account_id"], ["accounts.account_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("position_id", name=op.f("pk_positions")),
        sa.UniqueConstraint("account_id", "instrument", name="uq_positions_account_instrument"),
    )
    op.create_index("ix_positions_account_instrument", "positions", ["account_id", "instrument"], unique=False)

    op.create_table(
        "balance_snapshots",
        sa.Column("snapshot_id", sa.String(length=36), nullable=False),
        sa.Column("account_id", sa.String(length=36), nullable=False),
        sa.Column("currency", sa.String(length=16), nullable=False),
        sa.Column("total", sa.Float(), nullable=False),
        sa.Column("available", sa.Float(), nullable=False),
        sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["account_id"], ["accounts.account_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("snapshot_id", name=op.f("pk_balance_snapshots")),
    )
    op.create_index(op.f("ix_balance_snapshots_account_id"), "balance_snapshots", ["account_id"], unique=False)
    op.create_index(op.f("ix_balance_snapshots_captured_at"), "balance_snapshots", ["captured_at"], unique=False)

    op.create_table(
        "domain_events",
        sa.Column("event_id", sa.String(length=36), nullable=False),
        sa.Column("event_type", sa.String(length=128), nullable=False),
        sa.Column("event_version", sa.Integer(), nullable=False),
        sa.Column("aggregate_type", sa.String(length=64), nullable=False),
        sa.Column("aggregate_id", sa.String(length=36), nullable=False),
        sa.Column("strategy_id", sa.String(length=36), nullable=True),
        sa.Column("deployment_id", sa.String(length=36), nullable=True),
        sa.Column("account_id", sa.String(length=36), nullable=True),
        sa.Column("venue", sa.String(length=64), nullable=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("correlation_id", sa.String(length=64), nullable=False),
        sa.Column("causation_id", sa.String(length=64), nullable=True),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=False),
        sa.Column("published", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("event_id", name=op.f("pk_domain_events")),
    )
    op.create_index(op.f("ix_domain_events_account_id"), "domain_events", ["account_id"], unique=False)
    op.create_index(op.f("ix_domain_events_aggregate_id"), "domain_events", ["aggregate_id"], unique=False)
    op.create_index(op.f("ix_domain_events_aggregate_type"), "domain_events", ["aggregate_type"], unique=False)
    op.create_index(op.f("ix_domain_events_correlation_id"), "domain_events", ["correlation_id"], unique=False)
    op.create_index(op.f("ix_domain_events_deployment_id"), "domain_events", ["deployment_id"], unique=False)
    op.create_index(op.f("ix_domain_events_event_type"), "domain_events", ["event_type"], unique=False)
    op.create_index(op.f("ix_domain_events_published"), "domain_events", ["published"], unique=False)
    op.create_index(op.f("ix_domain_events_strategy_id"), "domain_events", ["strategy_id"], unique=False)
    op.create_index(op.f("ix_domain_events_timestamp"), "domain_events", ["timestamp"], unique=False)
    op.create_index("ix_events_type_time", "domain_events", ["event_type", "timestamp"], unique=False)
    op.create_index(
        "ix_events_aggregate_time",
        "domain_events",
        ["aggregate_type", "aggregate_id", "timestamp"],
        unique=False,
    )

    op.create_table(
        "reconciliation_issues",
        sa.Column("issue_id", sa.String(length=36), nullable=False),
        sa.Column("account_id", sa.String(length=36), nullable=False),
        sa.Column("issue_type", sa.String(length=64), nullable=False),
        sa.Column("severity", sa.String(length=32), nullable=False),
        sa.Column("details", sa.JSON(), nullable=False),
        sa.Column("detected_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["account_id"], ["accounts.account_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("issue_id", name=op.f("pk_reconciliation_issues")),
    )
    op.create_index(op.f("ix_reconciliation_issues_account_id"), "reconciliation_issues", ["account_id"], unique=False)
    op.create_index(op.f("ix_reconciliation_issues_detected_at"), "reconciliation_issues", ["detected_at"], unique=False)
    op.create_index(op.f("ix_reconciliation_issues_issue_type"), "reconciliation_issues", ["issue_type"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_reconciliation_issues_issue_type"), table_name="reconciliation_issues")
    op.drop_index(op.f("ix_reconciliation_issues_detected_at"), table_name="reconciliation_issues")
    op.drop_index(op.f("ix_reconciliation_issues_account_id"), table_name="reconciliation_issues")
    op.drop_table("reconciliation_issues")

    op.drop_index("ix_events_aggregate_time", table_name="domain_events")
    op.drop_index("ix_events_type_time", table_name="domain_events")
    op.drop_index(op.f("ix_domain_events_timestamp"), table_name="domain_events")
    op.drop_index(op.f("ix_domain_events_strategy_id"), table_name="domain_events")
    op.drop_index(op.f("ix_domain_events_published"), table_name="domain_events")
    op.drop_index(op.f("ix_domain_events_event_type"), table_name="domain_events")
    op.drop_index(op.f("ix_domain_events_deployment_id"), table_name="domain_events")
    op.drop_index(op.f("ix_domain_events_correlation_id"), table_name="domain_events")
    op.drop_index(op.f("ix_domain_events_aggregate_type"), table_name="domain_events")
    op.drop_index(op.f("ix_domain_events_aggregate_id"), table_name="domain_events")
    op.drop_index(op.f("ix_domain_events_account_id"), table_name="domain_events")
    op.drop_table("domain_events")

    op.drop_index(op.f("ix_balance_snapshots_captured_at"), table_name="balance_snapshots")
    op.drop_index(op.f("ix_balance_snapshots_account_id"), table_name="balance_snapshots")
    op.drop_table("balance_snapshots")

    op.drop_index("ix_positions_account_instrument", table_name="positions")
    op.drop_table("positions")

    op.drop_index(op.f("ix_fills_order_id"), table_name="fills")
    op.drop_table("fills")

    op.drop_index("ix_orders_account_status", table_name="orders")
    op.drop_index(op.f("ix_orders_venue_order_id"), table_name="orders")
    op.drop_index(op.f("ix_orders_intent_id"), table_name="orders")
    op.drop_index(op.f("ix_orders_account_id"), table_name="orders")
    op.drop_table("orders")

    op.drop_index(op.f("ix_order_intents_strategy_id"), table_name="order_intents")
    op.drop_index(op.f("ix_order_intents_deployment_id"), table_name="order_intents")
    op.drop_index(op.f("ix_order_intents_created_at"), table_name="order_intents")
    op.drop_index(op.f("ix_order_intents_account_id"), table_name="order_intents")
    op.drop_table("order_intents")

    op.drop_index("ix_deployments_strategy_status", table_name="strategy_deployments")
    op.drop_table("strategy_deployments")

    op.drop_table("strategies")
    op.drop_index(op.f("ix_accounts_venue"), table_name="accounts")
    op.drop_table("accounts")

    sa.Enum(name="orderstatusdb").drop(op.get_bind(), checkfirst=False)
    sa.Enum(name="orderintentstatusdb").drop(op.get_bind(), checkfirst=False)
    sa.Enum(name="strategydeploymentstatus").drop(op.get_bind(), checkfirst=False)
