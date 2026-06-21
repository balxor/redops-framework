from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AuditLogRead(BaseModel):
    audit_log_id: str
    project_id: str
    actor_user_id: str
    action: str
    resource_type: str
    resource_id: str | None
    summary: str
    detail: dict[str, str | int | float | bool | None] = Field(default_factory=dict)
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
