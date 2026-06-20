from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

AssetType = Literal["domain", "ip_address", "url", "application", "host", "service", "other"]
Criticality = Literal["unknown", "low", "medium", "high", "critical"]


class AssetBase(BaseModel):
    value: str = Field(min_length=1, max_length=500)
    type: AssetType
    scope_id: str | None = None
    environment: str | None = Field(default=None, max_length=100)
    criticality: Criticality = "unknown"
    tags: list[str] = Field(default_factory=list)
    metadata: dict[str, str | int | float | bool | None] = Field(default_factory=dict)


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    value: str | None = Field(default=None, min_length=1, max_length=500)
    type: AssetType | None = None
    scope_id: str | None = None
    environment: str | None = Field(default=None, max_length=100)
    criticality: Criticality | None = None
    tags: list[str] | None = None
    metadata: dict[str, str | int | float | bool | None] | None = None


class AssetRead(AssetBase):
    asset_id: str
    project_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

