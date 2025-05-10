from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr

from rest_enum.user_enum import UserRole, UserStatus

# Pydantic 스키마 정의
class UserCreate(BaseModel):
    login_id: str
    role: UserRole
    status: UserStatus
    email: str
    name: str
    profile_img: Optional[str] = None


# Pydantic 스키마 정의
class UserRead(BaseModel):
    id: UUID
    login_id: str
    role: UserRole
    status: UserStatus
    email: str
    name: str
    profile_img: Optional[str] = None

    model_config = {
        'from_attributes': True
    }
