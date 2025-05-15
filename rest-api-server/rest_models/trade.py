from datetime import datetime
from uuid import UUID as PyUUID, uuid4

from sqlalchemy import Integer, DateTime, UUID as SqlUUID
from sqlalchemy.orm import Mapped, mapped_column

from rest_models.base import Base


class Trade(Base):
    __tablename__ = "trades"

    id: Mapped[PyUUID] = mapped_column(SqlUUID(as_uuid=True), primary_key=True, default=uuid4)

    buy_order_id: Mapped[PyUUID] = mapped_column(SqlUUID, nullable=False, index=True)
    sell_order_id: Mapped[PyUUID] = mapped_column(SqlUUID, nullable=False, index=True)

    stock_id: Mapped[PyUUID] = mapped_column(SqlUUID, nullable=False, index=True)
    price: Mapped[float] = mapped_column(Integer, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)