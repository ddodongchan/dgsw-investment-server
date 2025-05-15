from datetime import datetime

from pydantic import BaseModel

from rest_enum.order_enum import OrderType


class OrderCreate(BaseModel):
    user_id: int
    type: OrderType
    stock_id: str
    amount: int
    price: float
    timestamp: datetime