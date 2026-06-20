from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

ProjectRole = Literal["lead_operator", "operator", "reviewer", "client_viewer"]


class ProjectMemberCreate(BaseModel):
    user_id: str
    project_role: ProjectRole


class ProjectMemberUpdate(BaseModel):
    project_role: ProjectRole


class ProjectMemberRead(BaseModel):
    project_member_id: str
    project_id: str
    user_id: str
    project_role: ProjectRole
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

