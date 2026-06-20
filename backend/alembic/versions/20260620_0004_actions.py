"""actions

Revision ID: 20260620_0004
Revises: 20260620_0003
Create Date: 2026-06-20
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "20260620_0004"
down_revision: str | None = "20260620_0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "actions",
        sa.Column("action_id", sa.String(length=128), primary_key=True),
        sa.Column("project_id", sa.String(length=128), sa.ForeignKey("projects.project_id", ondelete="CASCADE"), nullable=False),
        sa.Column("campaign_id", sa.String(length=128), nullable=True),
        sa.Column("campaign_step_id", sa.String(length=128), nullable=True),
        sa.Column("asset_id", sa.String(length=128), nullable=True),
        sa.Column("operator_id", sa.String(length=128), nullable=False),
        sa.Column("action_type", sa.String(length=80), nullable=False),
        sa.Column("action_summary", sa.String(length=500), nullable=False),
        sa.Column("action_detail", sa.Text(), nullable=True),
        sa.Column("result", sa.String(length=80), nullable=False),
        sa.Column("detection_status", sa.String(length=80), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_actions_project_id", "actions", ["project_id"])
    op.create_index("ix_actions_campaign_step_id", "actions", ["campaign_step_id"])


def downgrade() -> None:
    op.drop_index("ix_actions_campaign_step_id", table_name="actions")
    op.drop_index("ix_actions_project_id", table_name="actions")
    op.drop_table("actions")

