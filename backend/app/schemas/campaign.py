from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

CampaignStatus = Literal["draft", "planned", "approved", "active", "completed", "cancelled"]
StepStatus = Literal["planned", "approved", "executed", "blocked", "skipped", "detected", "not_detected"]


class CampaignStep(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    attack_technique_id: str | None = Field(default=None, max_length=50)
    status: StepStatus = "planned"
    approval_required: bool = True
    notes: str | None = Field(default=None, max_length=4000)


class CampaignBase(BaseModel):
    name: str = Field(min_length=3, max_length=200)
    objective: str = Field(min_length=3, max_length=2000)
    status: CampaignStatus = "draft"
    steps: list[CampaignStep] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    metadata: dict[str, str | int | float | bool | None] = Field(default_factory=dict)


class CampaignCreate(CampaignBase):
    pass


class CampaignUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=200)
    objective: str | None = Field(default=None, min_length=3, max_length=2000)
    status: CampaignStatus | None = None
    steps: list[CampaignStep] | None = None
    tags: list[str] | None = None
    metadata: dict[str, str | int | float | bool | None] | None = None


class CampaignRead(CampaignBase):
    campaign_id: str
    project_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

