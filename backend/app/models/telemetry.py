from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Telemetry(Base):
    __tablename__ = "telemetry"

    telemetry_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.project_id", ondelete="CASCADE"), nullable=False)
    campaign_id: Mapped[str | None] = mapped_column(String(128))
    campaign_step_id: Mapped[str | None] = mapped_column(String(128))
    action_id: Mapped[str | None] = mapped_column(String(128))
    finding_id: Mapped[str | None] = mapped_column(String(128))
    asset_id: Mapped[str | None] = mapped_column(String(128))
    evidence_id: Mapped[str | None] = mapped_column(String(128))
    attack_technique_id: Mapped[str | None] = mapped_column(String(50))
    expected_telemetry: Mapped[list[dict]] = mapped_column(JSON, nullable=False, default=list)
    observed_telemetry: Mapped[list[dict]] = mapped_column(JSON, nullable=False, default=list)
    data_source: Mapped[str | None] = mapped_column(String(120))
    detection_status: Mapped[str] = mapped_column(String(80), nullable=False, default="unknown")
    review_note: Mapped[str | None] = mapped_column(Text)
    reviewed_by: Mapped[str | None] = mapped_column(String(128))
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
