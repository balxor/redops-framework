from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ReportStatus = Literal["draft", "generated", "under_review", "approved", "final", "archived"]
ReportFormat = Literal["markdown", "html", "pdf", "docx_later"]


class ReportSection(BaseModel):
    key: str = Field(min_length=1, max_length=100)
    title: str = Field(min_length=1, max_length=200)
    content: str | None = Field(default=None, max_length=20000)
    order: int = Field(default=0, ge=0)


class ReportBase(BaseModel):
    title: str = Field(min_length=3, max_length=300)
    version: str = Field(default="0.1", min_length=1, max_length=40)
    status: ReportStatus = "draft"
    format: ReportFormat = "markdown"
    file_path: str | None = Field(default=None, max_length=1000)
    finding_ids: list[str] = Field(default_factory=list)
    evidence_ids: list[str] = Field(default_factory=list)
    sections: list[ReportSection] = Field(default_factory=list)
    prepared_by: str | None = None
    reviewed_by: str | None = None
    generated_by: str | None = None
    generated_at: datetime | None = None
    published_at: datetime | None = None
    metadata: dict[str, str | int | float | bool | None] = Field(default_factory=dict)


class ReportCreate(ReportBase):
    pass


class ReportGenerateRequest(BaseModel):
    title: str = Field(default="Project Report Outline", min_length=3, max_length=300)
    format: ReportFormat = "markdown"
    include_sections: list[str] = Field(default_factory=list)


class ReportUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=300)
    version: str | None = Field(default=None, min_length=1, max_length=40)
    status: ReportStatus | None = None
    format: ReportFormat | None = None
    file_path: str | None = Field(default=None, max_length=1000)
    finding_ids: list[str] | None = None
    evidence_ids: list[str] | None = None
    sections: list[ReportSection] | None = None
    prepared_by: str | None = None
    reviewed_by: str | None = None
    generated_by: str | None = None
    generated_at: datetime | None = None
    published_at: datetime | None = None
    metadata: dict[str, str | int | float | bool | None] | None = None


class ReportRead(ReportBase):
    report_id: str
    project_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
