from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

EvidenceType = Literal[
    "screenshot",
    "terminal_output",
    "log_file",
    "log_excerpt",
    "http_request_response",
    "scanner_output",
    "configuration_export",
    "siem_alert",
    "edr_alert",
    "file_hash",
    "document",
    "manual_note",
    "report_reference",
    "other",
]


class EvidenceBase(BaseModel):
    action_id: str | None = None
    finding_id: str | None = None
    asset_id: str | None = None
    evidence_type: EvidenceType
    file_name: str | None = Field(default=None, max_length=500)
    file_size: int | None = Field(default=None, ge=0)
    mime_type: str | None = Field(default=None, max_length=200)
    file_hash_sha256: str | None = Field(default=None, min_length=64, max_length=64)
    description: str = Field(min_length=3, max_length=8000)
    sanitized: bool = True
    captured_at: datetime | None = None
    metadata: dict[str, str | int | float | bool | None] = Field(default_factory=dict)


class EvidenceCreate(EvidenceBase):
    pass


class EvidenceUpdate(BaseModel):
    action_id: str | None = None
    finding_id: str | None = None
    asset_id: str | None = None
    evidence_type: EvidenceType | None = None
    file_name: str | None = Field(default=None, max_length=500)
    file_size: int | None = Field(default=None, ge=0)
    mime_type: str | None = Field(default=None, max_length=200)
    file_hash_sha256: str | None = Field(default=None, min_length=64, max_length=64)
    description: str | None = Field(default=None, min_length=3, max_length=8000)
    sanitized: bool | None = None
    captured_at: datetime | None = None
    metadata: dict[str, str | int | float | bool | None] | None = None


class EvidenceRead(EvidenceBase):
    evidence_id: str
    project_id: str
    uploaded_by: str
    uploaded_at: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

