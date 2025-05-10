from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    REPORTER = "REPORTER"

class UserStatus(str, Enum):
    ACTIVATE = "ACTIVATE"
    DEACTIVATE = "DEACTIVATE"

# Pydantic 스키마 정의
class UserCreate(BaseModel):
    login_id: str
    role: UserRole
    status: UserStatus
    email: EmailStr
    name: str
    profile_img: Optional[str] = None

# Pydantic 스키마 정의
class UserRead(BaseModel):
    id: UUID
    login_id: str
    role: UserRole
    status: UserStatus
    email: EmailStr
    name: str
    profile_img: Optional[str] = None