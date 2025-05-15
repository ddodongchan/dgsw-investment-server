from datetime import datetime, timezone
from uuid import UUID, uuid4

from rest_models.base import Base
from rest_models.user import User
from sqlalchemy import String, DateTime, ForeignKey, Integer
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship



class News(Base):
    __tablename__ = "news"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    context: Mapped[str] = mapped_column(String(2000), nullable=False)
    read: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)  # 수정된 부분
    )
    user = relationship(User, backref='news')