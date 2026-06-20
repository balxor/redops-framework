from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Severity = Literal["informational", "low", "medium", "high", "critical"]
FindingStatus = Literal["draft", "under_review", "confirmed", "risk_accepted", "remediated", "closed"]
Likelihood = Literal["unknown", "low", "medium", "high"]


class AttackMapping(BaseModel):
    technique_id: str = Field(min_length=1, max_length=50)
    tactic: str | None = Field(default=None, max_length=100)
    notes: str | None = Field(default=None, max_length=1000)


class FindingBase(BaseModel):
    title: str = Field(min_length=3, max_length=300)
    summary: str | None = Field(default=None, max_length=8000)
    severity: Severity
    status: FindingStatus = "draft"
    affected_assets: list[str] = Field(default_factory=list)
    attack_technique_id: str | None = Field(default=None, max_length=50)
    attack_mapping: list[AttackMapping] = Field(default_factory=list)
    evidence_ids: list[str] = Field(default_factory=list)
    impact: str | None = Field(default=None, max_length=8000)
    likelihood: Likelihood = "unknown"
    recommendation: str | None = Field(default=None, max_length=8000)
    reviewed_by: str | None = None
    metadata: dict[str, str | int | float | bool | None] = Field(default_factory=dict)


class FindingCreate(FindingBase):
    pass


class FindingUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=300)
    summary: str | None = Field(default=None, max_length=8000)
    severity: Severity | None = None
    status: FindingStatus | None = None
    affected_assets: list[str] | None = None
    attack_technique_id: str | None = Field(default=None, max_length=50)
    attack_mapping: list[AttackMapping] | None = None
    evidence_ids: list[str] | None = None
    impact: str | None = Field(default=None, max_length=8000)
    likelihood: Likelihood | None = None
    recommendation: str | None = Field(default=None, max_length=8000)
    reviewed_by: str | None = None
    metadata: dict[str, str | int | float | bool | None] | None = None


class FindingRead(FindingBase):
    finding_id: str
    project_id: str
    created_by: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

