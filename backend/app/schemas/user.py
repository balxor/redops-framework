from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

RoleName = Literal["admin", "lead_operator", "operator", "reviewer", "client_viewer"]


class CurrentUser(BaseModel):
    user_id: str
    email: EmailStr
    full_name: str
    roles: list[str] = Field(default_factory=list)
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class UserRead(CurrentUser):
    created_at: datetime
    updated_at: datetime
    last_login_at: datetime | None = None


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=200)
    password: str = Field(min_length=8, max_length=200)
    roles: list[RoleName] = Field(default_factory=lambda: ["operator"])
    is_active: bool = True


class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=200)
    password: str | None = Field(default=None, min_length=8, max_length=200)
    roles: list[RoleName] | None = None
    is_active: bool | None = None
