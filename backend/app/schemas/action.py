from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ActionType = Literal[
    "manual_validation",
    "configuration_review",
    "recon_note",
    "scanner_result",
    "exploit_validation_note",
    "access_validation_note",
    "detection_validation_note",
    "cleanup_note",
]
ActionResult = Literal["unknown", "planned", "approved", "executed", "skipped", "failed"]
DetectionStatus = Literal["unknown", "detected", "not_detected", "blocked", "partially_detected", "not_applicable"]


class ActionBase(BaseModel):
    campaign_id: str | None = None
    campaign_step_id: str | None = None
    asset_id: str | None = None
    action_type: ActionType
    action_summary: str = Field(min_length=3, max_length=500)
    action_detail: str | None = Field(default=None, max_length=8000)
    result: ActionResult = "unknown"
    detection_status: DetectionStatus = "unknown"
    started_at: datetime | None = None
    ended_at: datetime | None = None
    metadata: dict[str, str | int | float | bool | None] = Field(default_factory=dict)


class ActionCreate(ActionBase):
    pass


class ActionUpdate(BaseModel):
    campaign_id: str | None = None
    campaign_step_id: str | None = None
    asset_id: str | None = None
    action_type: ActionType | None = None
    action_summary: str | None = Field(default=None, min_length=3, max_length=500)
    action_detail: str | None = Field(default=None, max_length=8000)
    result: ActionResult | None = None
    detection_status: DetectionStatus | None = None
    started_at: datetime | None = None
    ended_at: datetime | None = None
    metadata: dict[str, str | int | float | bool | None] | None = None


class ActionRead(ActionBase):
    action_id: str
    project_id: str
    operator_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

