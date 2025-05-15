from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, model_validator

from ws_enum.order_enum import OrderType, OrderKind


class Order(BaseModel):
    order_id: UUID = None
    user_id: UUID
    type: OrderType
    stock_id: UUID
    amount: int
    price: float
    timestamp: datetime
    kind: OrderKind

    @model_validator(mode='before')
    def set_order_id(cls, values):
        if values.get('order_id') is None:
            values['order_id'] = uuid4()
        return values