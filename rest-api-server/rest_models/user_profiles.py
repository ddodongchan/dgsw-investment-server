from uuid import UUID, uuid4
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    pass

class UserProfile(Base):
    __tablename__ = "user_profile"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_credential_id: Mapped[UUID] = mapped_column(
        ForeignKey("user_credential.id", ondelete="CASCADE"), nullable=False
    )
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    profile_img: Mapped[str] = mapped_column(String(255), nullable=True)