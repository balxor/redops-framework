from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ApprovalStatus = Literal["pending", "approved", "rejected", "revoked", "expired"]
ApprovalRiskLevel = Literal["standard", "controlled", "sensitive", "high_risk"]
ApprovalEntityType = Literal["campaign", "action_type", "scope", "policy_exception"]


class ApprovalBase(BaseModel):
    entity_type: ApprovalEntityType
    entity_id: str = Field(min_length=1, max_length=128)
    risk_level: ApprovalRiskLevel = "controlled"
    reason: str = Field(min_length=3, max_length=4000)
    conditions: dict[str, str | int | float | bool | None] = Field(default_factory=dict)
    expires_at: datetime | None = None


class ApprovalCreate(ApprovalBase):
    pass


class ApprovalDecision(BaseModel):
    decision_note: str | None = Field(default=None, max_length=4000)


class ApprovalRead(ApprovalBase):
    approval_id: str
    project_id: str
    status: ApprovalStatus
    requested_by: str
    decided_by: str | None
    decision_note: str | None
    requested_at: datetime
    decided_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
