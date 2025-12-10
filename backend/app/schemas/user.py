from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.core.constants import RoleEnum
from app.schemas.common import TimestampBase

class RoleResponse(BaseModel):
    id: int
    name: RoleEnum
    permissions: list[str]
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=2)
    role: RoleEnum = RoleEnum.ADMIN

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[RoleEnum] = None
    is_active: Optional[bool] = None

class UserResponse(TimestampBase):
    id: int
    email: str
    full_name: str
    role: RoleResponse
    is_active: bool
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
