"""telemetry and detection gaps

Revision ID: 20260620_0011
Revises: 20260620_0010
Create Date: 2026-06-20
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "20260620_0011"
down_revision: str | None = "20260620_0010"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "telemetry",
        sa.Column("telemetry_id", sa.String(length=128), primary_key=True),
        sa.Column("project_id", sa.String(length=128), sa.ForeignKey("projects.project_id", ondelete="CASCADE"), nullable=False),
        sa.Column("campaign_id", sa.String(length=128), nullable=True),
        sa.Column("campaign_step_id", sa.String(length=128), nullable=True),
        sa.Column("action_id", sa.String(length=128), nullable=True),
        sa.Column("finding_id", sa.String(length=128), nullable=True),
        sa.Column("asset_id", sa.String(length=128), nullable=True),
        sa.Column("evidence_id", sa.String(length=128), nullable=True),
        sa.Column("attack_technique_id", sa.String(length=50), nullable=True),
        sa.Column("expected_telemetry", sa.JSON(), nullable=False),
        sa.Column("observed_telemetry", sa.JSON(), nullable=False),
        sa.Column("data_source", sa.String(length=120), nullable=True),
        sa.Column("detection_status", sa.String(length=80), nullable=False),
        sa.Column("review_note", sa.Text(), nullable=True),
        sa.Column("reviewed_by", sa.String(length=128), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_telemetry_project_id", "telemetry", ["project_id"])
    op.create_index("ix_telemetry_detection_status", "telemetry", ["detection_status"])

    op.create_table(
        "detection_gaps",
        sa.Column("gap_id", sa.String(length=128), primary_key=True),
        sa.Column("project_id", sa.String(length=128), sa.ForeignKey("projects.project_id", ondelete="CASCADE"), nullable=False),
        sa.Column("telemetry_id", sa.String(length=128), nullable=True),
        sa.Column("campaign_step_id", sa.String(length=128), nullable=True),
        sa.Column("finding_id", sa.String(length=128), nullable=True),
        sa.Column("evidence_id", sa.String(length=128), nullable=True),
        sa.Column("asset_id", sa.String(length=128), nullable=True),
        sa.Column("attack_technique_id", sa.String(length=50), nullable=True),
        sa.Column("gap_type", sa.String(length=80), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("impact", sa.Text(), nullable=True),
        sa.Column("recommendation", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("created_by", sa.String(length=128), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_detection_gaps_project_id", "detection_gaps", ["project_id"])
    op.create_index("ix_detection_gaps_status", "detection_gaps", ["status"])


def downgrade() -> None:
    op.drop_index("ix_detection_gaps_status", table_name="detection_gaps")
    op.drop_index("ix_detection_gaps_project_id", table_name="detection_gaps")
    op.drop_table("detection_gaps")
    op.drop_index("ix_telemetry_detection_status", table_name="telemetry")
    op.drop_index("ix_telemetry_project_id", table_name="telemetry")
    op.drop_table("telemetry")
