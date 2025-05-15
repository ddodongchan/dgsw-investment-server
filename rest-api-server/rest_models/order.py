from datetime import datetime
from uuid import UUID as PyUUID, uuid4

from sqlalchemy import Integer, Float, DateTime, Enum as SqlEnum
from sqlalchemy import UUID as SqlUUID
from sqlalchemy.orm import Mapped, mapped_column

from rest_enum.order_enum import OrderType, OrderStatus, OrderKind
from rest_models.base import Base


# Order 모델 정의
class Order(Base):
    __tablename__ = "orders"

    # 주문 아이디 (Primary Key)
    id: Mapped[PyUUID] = mapped_column(SqlUUID(as_uuid=True), primary_key=True, default=uuid4)

    # 사용자 아이디
    user_id: Mapped[PyUUID] = mapped_column(SqlUUID, nullable=False, index=True)

    # 주문 유형 (매수, 매도 등)
    type: Mapped[OrderType] = mapped_column(SqlEnum(OrderType), nullable=False)

    # 체결 여부
    status: Mapped[OrderStatus] = mapped_column(SqlEnum(OrderStatus), nullable=False)

    # 주식 코드
    stock_id: Mapped[PyUUID] = mapped_column(SqlUUID, nullable=False, index=True)

    # 주문 수량
    amount: Mapped[int] = mapped_column(Integer)

    filled: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # 주문 가격
    price: Mapped[float] = mapped_column(Float)

    # 주문 시간 (기본값은 현재 시간)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    kind: Mapped[OrderKind] = mapped_column(SqlEnum(OrderKind), nullable=False)