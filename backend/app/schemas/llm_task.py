from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

LlmTaskType = Literal[
    "scope_summary",
    "attack_mapping_suggestion",
    "campaign_plan_draft",
    "policy_review",
    "evidence_summary",
    "finding_draft",
    "remediation_draft",
    "report_draft",
    "telemetry_gap_analysis",
    "cleanup_checklist",
    "terminology_review",
]
LlmTaskStatus = Literal["under_review", "accepted", "rejected", "archived"]


class LlmTaskBase(BaseModel):
    task_type: LlmTaskType
    entity_type: str | None = Field(default=None, max_length=80)
    entity_id: str | None = Field(default=None, max_length=128)
    input_summary: str = Field(min_length=3, max_length=8000)
    output_content: str = Field(min_length=3, max_length=20000)
    assumptions: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    requires_review: bool = True


class LlmTaskCreate(LlmTaskBase):
    pass


class LlmTaskReview(BaseModel):
    review_note: str | None = Field(default=None, max_length=4000)


class LlmTaskRead(LlmTaskBase):
    llm_task_id: str
    project_id: str
    status: LlmTaskStatus
    requested_by: str
    reviewed_by: str | None
    review_note: str | None
    reviewed_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
