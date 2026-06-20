from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ProjectStatus = Literal["draft", "active", "paused", "completed", "archived"]
EngagementType = Literal[
    "external_pentest",
    "internal_pentest",
    "web_application_pentest",
    "mobile_application_pentest",
    "cloud_security_assessment",
    "red_team",
    "assumed_breach",
    "purple_team",
    "internal_assessment",
]


class ProjectBase(BaseModel):
    name: str = Field(min_length=3, max_length=200)
    engagement_type: EngagementType
    status: ProjectStatus = "draft"
    client_name: str | None = Field(default=None, max_length=200)
    description: str | None = Field(default=None, max_length=4000)
    start_date: date | None = None
    end_date: date | None = None
    timezone: str | None = Field(default=None, max_length=100)
    tags: list[str] = Field(default_factory=list)
    metadata: dict[str, str | int | float | bool | None] = Field(default_factory=dict)


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=200)
    engagement_type: EngagementType | None = None
    status: ProjectStatus | None = None
    client_name: str | None = Field(default=None, max_length=200)
    description: str | None = Field(default=None, max_length=4000)
    start_date: date | None = None
    end_date: date | None = None
    timezone: str | None = Field(default=None, max_length=100)
    tags: list[str] | None = None
    metadata: dict[str, str | int | float | bool | None] | None = None


class ProjectRead(ProjectBase):
    project_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

