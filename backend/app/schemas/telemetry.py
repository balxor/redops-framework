from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

DetectionStatus = Literal["unknown", "detected", "not_detected", "blocked", "partially_detected", "not_applicable"]
GapType = Literal[
    "missing_telemetry",
    "incomplete_telemetry",
    "delayed_telemetry",
    "low_confidence_signal",
    "missing_data_source",
    "missing_detection_rule",
    "blocked_before_detection",
    "not_reviewed",
]
GapStatus = Literal["open", "under_review", "accepted", "resolved", "closed"]


class TelemetrySignal(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    data_source: str | None = Field(default=None, max_length=120)
    data_component: str | None = Field(default=None, max_length=200)
    signal: str | None = Field(default=None, max_length=2000)
    required: bool = True


class TelemetryBase(BaseModel):
    campaign_id: str | None = None
    campaign_step_id: str | None = None
    action_id: str | None = None
    finding_id: str | None = None
    asset_id: str | None = None
    evidence_id: str | None = None
    attack_technique_id: str | None = Field(default=None, max_length=50)
    expected_telemetry: list[TelemetrySignal] = Field(default_factory=list)
    observed_telemetry: list[TelemetrySignal] = Field(default_factory=list)
    data_source: str | None = Field(default=None, max_length=120)
    detection_status: DetectionStatus = "unknown"
    review_note: str | None = Field(default=None, max_length=8000)
    reviewed_by: str | None = None
    reviewed_at: datetime | None = None


class TelemetryCreate(TelemetryBase):
    pass


class TelemetryUpdate(BaseModel):
    campaign_id: str | None = None
    campaign_step_id: str | None = None
    action_id: str | None = None
    finding_id: str | None = None
    asset_id: str | None = None
    evidence_id: str | None = None
    attack_technique_id: str | None = Field(default=None, max_length=50)
    expected_telemetry: list[TelemetrySignal] | None = None
    observed_telemetry: list[TelemetrySignal] | None = None
    data_source: str | None = Field(default=None, max_length=120)
    detection_status: DetectionStatus | None = None
    review_note: str | None = Field(default=None, max_length=8000)
    reviewed_by: str | None = None
    reviewed_at: datetime | None = None


class TelemetryRead(TelemetryBase):
    telemetry_id: str
    project_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DetectionGapBase(BaseModel):
    telemetry_id: str | None = None
    campaign_step_id: str | None = None
    finding_id: str | None = None
    evidence_id: str | None = None
    asset_id: str | None = None
    attack_technique_id: str | None = Field(default=None, max_length=50)
    gap_type: GapType
    summary: str = Field(min_length=3, max_length=8000)
    impact: str | None = Field(default=None, max_length=8000)
    recommendation: str | None = Field(default=None, max_length=8000)
    status: GapStatus = "open"


class DetectionGapCreate(DetectionGapBase):
    pass


class DetectionGapUpdate(BaseModel):
    telemetry_id: str | None = None
    campaign_step_id: str | None = None
    finding_id: str | None = None
    evidence_id: str | None = None
    asset_id: str | None = None
    attack_technique_id: str | None = Field(default=None, max_length=50)
    gap_type: GapType | None = None
    summary: str | None = Field(default=None, min_length=3, max_length=8000)
    impact: str | None = Field(default=None, max_length=8000)
    recommendation: str | None = Field(default=None, max_length=8000)
    status: GapStatus | None = None


class DetectionGapRead(DetectionGapBase):
    gap_id: str
    project_id: str
    created_by: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
