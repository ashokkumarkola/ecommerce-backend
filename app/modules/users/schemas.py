from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    phone: str | None = None


class UserUpdate(BaseModel):
    phone: str | None = None
    is_active: bool | None = None
    is_verified: bool | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
    phone: str | None
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime