from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


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

