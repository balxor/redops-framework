from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Action(Base):
    __tablename__ = "actions"

    action_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.project_id", ondelete="CASCADE"), nullable=False)
    campaign_id: Mapped[str | None] = mapped_column(String(128))
    campaign_step_id: Mapped[str | None] = mapped_column(String(128))
    asset_id: Mapped[str | None] = mapped_column(String(128))
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    action_type: Mapped[str] = mapped_column(String(80), nullable=False)
    action_summary: Mapped[str] = mapped_column(String(500), nullable=False)
    action_detail: Mapped[str | None] = mapped_column(Text)
    result: Mapped[str] = mapped_column(String(80), nullable=False, default="unknown")
    detection_status: Mapped[str] = mapped_column(String(80), nullable=False, default="unknown")
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    metadata_: Mapped[dict] = mapped_column("metadata", JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

