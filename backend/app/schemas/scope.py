from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ScopeStatus = Literal["draft", "pending_review", "approved", "expired", "revoked"]
TargetType = Literal[
    "ip_address",
    "ip_range",
    "domain",
    "subdomain",
    "url",
    "cloud_account",
    "repository",
    "wireless_network",
    "application",
    "api",
    "identity_tenant",
    "lab_environment",
]
Environment = Literal["production", "staging", "development", "lab", "unknown"]
RestrictedAction = Literal[
    "safe_validation_workflow",
    "exploit_validation",
    "credential_exposure_validation",
    "persistence_validation",
    "lateral_movement_validation",
    "egress_telemetry_validation",
    "external_tool_execution",
    "production_environment_validation",
]


class Target(BaseModel):
    type: TargetType
    value: str = Field(min_length=1, max_length=500)
    environment: Environment = "unknown"
    description: str | None = Field(default=None, max_length=1000)
    tags: list[str] = Field(default_factory=list)


class TestWindow(BaseModel):
    start: datetime
    end: datetime
    timezone: str | None = Field(default=None, max_length=100)


class ScopeBase(BaseModel):
    status: ScopeStatus = "draft"
    allowed_targets: list[Target] = Field(min_length=1)
    forbidden_targets: list[Target] = Field(default_factory=list)
    test_window: TestWindow
    rules_of_engagement: str | None = Field(default=None, max_length=8000)
    restricted_actions: list[RestrictedAction] = Field(default_factory=list)
    approval_required: bool = True
    notes: str | None = Field(default=None, max_length=4000)
    metadata: dict[str, str | int | float | bool | None] = Field(default_factory=dict)


class ScopeCreate(ScopeBase):
    pass


class ScopeUpdate(BaseModel):
    status: ScopeStatus | None = None
    allowed_targets: list[Target] | None = None
    forbidden_targets: list[Target] | None = None
    test_window: TestWindow | None = None
    rules_of_engagement: str | None = Field(default=None, max_length=8000)
    restricted_actions: list[RestrictedAction] | None = None
    approval_required: bool | None = None
    notes: str | None = Field(default=None, max_length=4000)
    metadata: dict[str, str | int | float | bool | None] | None = None


class ScopeRead(ScopeBase):
    scope_id: str
    project_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

