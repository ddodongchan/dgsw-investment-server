from uuid import UUID as PyUUID, uuid4

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import String
from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column

from rest_enum.user_enum import UserRole, UserStatus
from rest_models.base import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    login_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    role: Mapped[UserRole] = mapped_column(SqlEnum(UserRole), nullable=False)
    status: Mapped[UserStatus] = mapped_column(SqlEnum(UserStatus), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    profile_img: Mapped[str] = mapped_column(String(255), nullable=True)