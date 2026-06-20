from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Scope(Base):
    __tablename__ = "scopes"

    scope_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.project_id", ondelete="CASCADE"), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    allowed_targets: Mapped[list[dict]] = mapped_column(JSON, nullable=False, default=list)
    forbidden_targets: Mapped[list[dict]] = mapped_column(JSON, nullable=False, default=list)
    test_window: Mapped[dict] = mapped_column(JSON, nullable=False)
    rules_of_engagement: Mapped[str | None] = mapped_column(Text)
    restricted_actions: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    approval_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    notes: Mapped[str | None] = mapped_column(Text)
    metadata_: Mapped[dict] = mapped_column("metadata", JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

