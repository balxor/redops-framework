"""approvals

Revision ID: 20260620_0009
Revises: 20260620_0008
Create Date: 2026-06-20
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "20260620_0009"
down_revision: str | None = "20260620_0008"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "approvals",
        sa.Column("approval_id", sa.String(length=128), primary_key=True),
        sa.Column("project_id", sa.String(length=128), sa.ForeignKey("projects.project_id", ondelete="CASCADE"), nullable=False),
        sa.Column("entity_type", sa.String(length=80), nullable=False),
        sa.Column("entity_id", sa.String(length=128), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("risk_level", sa.String(length=40), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("conditions", sa.JSON(), nullable=False),
        sa.Column("requested_by", sa.String(length=128), nullable=False),
        sa.Column("decided_by", sa.String(length=128), nullable=True),
        sa.Column("decision_note", sa.Text(), nullable=True),
        sa.Column("requested_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_approvals_project_id", "approvals", ["project_id"])
    op.create_index("ix_approvals_status", "approvals", ["status"])
    op.create_index("ix_approvals_entity", "approvals", ["entity_type", "entity_id"])


def downgrade() -> None:
    op.drop_index("ix_approvals_entity", table_name="approvals")
    op.drop_index("ix_approvals_status", table_name="approvals")
    op.drop_index("ix_approvals_project_id", table_name="approvals")
    op.drop_table("approvals")
