from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class DetectionGap(Base):
    __tablename__ = "detection_gaps"

    gap_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.project_id", ondelete="CASCADE"), nullable=False)
    telemetry_id: Mapped[str | None] = mapped_column(String(128))
    campaign_step_id: Mapped[str | None] = mapped_column(String(128))
    finding_id: Mapped[str | None] = mapped_column(String(128))
    evidence_id: Mapped[str | None] = mapped_column(String(128))
    asset_id: Mapped[str | None] = mapped_column(String(128))
    attack_technique_id: Mapped[str | None] = mapped_column(String(50))
    gap_type: Mapped[str] = mapped_column(String(80), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    impact: Mapped[str | None] = mapped_column(Text)
    recommendation: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="open")
    created_by: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
