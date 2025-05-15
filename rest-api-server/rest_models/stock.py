from uuid import UUID as PyUUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float, UUID as SqlUUID
from rest_models.base import Base

class Stock(Base):
    __tablename__ = "stocks"
    id: Mapped[PyUUID] = mapped_column(SqlUUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String)
    current_price: Mapped[float] = mapped_column(Float)
    opening_price: Mapped[float] = mapped_column(Float)
    closing_price: Mapped[float] = mapped_column(Float)
    volume: Mapped[int] = mapped_column(Integer)
