"""evidence

Revision ID: 20260620_0005
Revises: 20260620_0004
Create Date: 2026-06-20
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "20260620_0005"
down_revision: str | None = "20260620_0004"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "evidence",
        sa.Column("evidence_id", sa.String(length=128), primary_key=True),
        sa.Column("project_id", sa.String(length=128), sa.ForeignKey("projects.project_id", ondelete="CASCADE"), nullable=False),
        sa.Column("action_id", sa.String(length=128), nullable=True),
        sa.Column("finding_id", sa.String(length=128), nullable=True),
        sa.Column("asset_id", sa.String(length=128), nullable=True),
        sa.Column("uploaded_by", sa.String(length=128), nullable=False),
        sa.Column("evidence_type", sa.String(length=80), nullable=False),
        sa.Column("file_name", sa.String(length=500), nullable=True),
        sa.Column("file_size", sa.Integer(), nullable=True),
        sa.Column("mime_type", sa.String(length=200), nullable=True),
        sa.Column("file_hash_sha256", sa.String(length=64), nullable=True),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("sanitized", sa.Boolean(), nullable=False),
        sa.Column("captured_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("uploaded_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_evidence_project_id", "evidence", ["project_id"])
    op.create_index("ix_evidence_action_id", "evidence", ["action_id"])


def downgrade() -> None:
    op.drop_index("ix_evidence_action_id", table_name="evidence")
    op.drop_index("ix_evidence_project_id", table_name="evidence")
    op.drop_table("evidence")

