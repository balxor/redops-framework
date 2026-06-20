"""initial tables

Revision ID: 20260620_0001
Revises:
Create Date: 2026-06-20
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "20260620_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "projects",
        sa.Column("project_id", sa.String(length=128), primary_key=True),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("engagement_type", sa.String(length=80), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("client_name", sa.String(length=200), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("timezone", sa.String(length=100), nullable=True),
        sa.Column("tags", sa.JSON(), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "scopes",
        sa.Column("scope_id", sa.String(length=128), primary_key=True),
        sa.Column("project_id", sa.String(length=128), sa.ForeignKey("projects.project_id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("allowed_targets", sa.JSON(), nullable=False),
        sa.Column("forbidden_targets", sa.JSON(), nullable=False),
        sa.Column("test_window", sa.JSON(), nullable=False),
        sa.Column("rules_of_engagement", sa.Text(), nullable=True),
        sa.Column("restricted_actions", sa.JSON(), nullable=False),
        sa.Column("approval_required", sa.Boolean(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "assets",
        sa.Column("asset_id", sa.String(length=128), primary_key=True),
        sa.Column("project_id", sa.String(length=128), sa.ForeignKey("projects.project_id", ondelete="CASCADE"), nullable=False),
        sa.Column("scope_id", sa.String(length=128), nullable=True),
        sa.Column("value", sa.String(length=500), nullable=False),
        sa.Column("type", sa.String(length=50), nullable=False),
        sa.Column("environment", sa.String(length=100), nullable=True),
        sa.Column("criticality", sa.String(length=32), nullable=False),
        sa.Column("tags", sa.JSON(), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "campaigns",
        sa.Column("campaign_id", sa.String(length=128), primary_key=True),
        sa.Column("project_id", sa.String(length=128), sa.ForeignKey("projects.project_id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("objective", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("steps", sa.JSON(), nullable=False),
        sa.Column("tags", sa.JSON(), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("campaigns")
    op.drop_table("assets")
    op.drop_table("scopes")
    op.drop_table("projects")

