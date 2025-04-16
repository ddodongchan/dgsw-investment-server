from enum import Enum
from uuid import UUID as PyUUID, uuid4
from sqlalchemy import Enum as SqlEnum

from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import String, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    REPORTER = "REPORTER"

class UserStatus(str, Enum):
    ACTIVATE = "ACTIVATE"
    DEACTIVATE = "DEACTIVATE"

class Base(AsyncAttrs, DeclarativeBase):
    pass

class UserCredential(Base):
    __tablename__ = "user_credential"
    id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    login_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    role: Mapped[UserRole] = mapped_column(SqlEnum(UserRole), nullable=False)
    status: Mapped[UserStatus] = mapped_column(SqlEnum(UserStatus), nullable=False)

