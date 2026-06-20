from pydantic import BaseModel, Field


class SafetySummary(BaseModel):
    project_id: str
    approved_scope_count: int
    has_approved_scope: bool
    restricted_actions: list[str] = Field(default_factory=list)

