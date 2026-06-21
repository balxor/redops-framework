"""llm tasks

Revision ID: 20260620_0010
Revises: 20260620_0009
Create Date: 2026-06-20
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "20260620_0010"
down_revision: str | None = "20260620_0009"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "llm_tasks",
        sa.Column("llm_task_id", sa.String(length=128), primary_key=True),
        sa.Column("project_id", sa.String(length=128), sa.ForeignKey("projects.project_id", ondelete="CASCADE"), nullable=False),
        sa.Column("task_type", sa.String(length=80), nullable=False),
        sa.Column("entity_type", sa.String(length=80), nullable=True),
        sa.Column("entity_id", sa.String(length=128), nullable=True),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("input_summary", sa.Text(), nullable=False),
        sa.Column("output_content", sa.Text(), nullable=False),
        sa.Column("assumptions", sa.JSON(), nullable=False),
        sa.Column("limitations", sa.JSON(), nullable=False),
        sa.Column("requires_review", sa.Boolean(), nullable=False),
        sa.Column("requested_by", sa.String(length=128), nullable=False),
        sa.Column("reviewed_by", sa.String(length=128), nullable=True),
        sa.Column("review_note", sa.Text(), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_llm_tasks_project_id", "llm_tasks", ["project_id"])
    op.create_index("ix_llm_tasks_status", "llm_tasks", ["status"])
    op.create_index("ix_llm_tasks_task_type", "llm_tasks", ["task_type"])


def downgrade() -> None:
    op.drop_index("ix_llm_tasks_task_type", table_name="llm_tasks")
    op.drop_index("ix_llm_tasks_status", table_name="llm_tasks")
    op.drop_index("ix_llm_tasks_project_id", table_name="llm_tasks")
    op.drop_table("llm_tasks")
