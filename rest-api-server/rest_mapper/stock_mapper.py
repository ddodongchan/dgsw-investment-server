from functools import singledispatchmethod

from rest_models.stock import Stock
from rest_models.user import User
from rest_schemas.stock import StockCreate
from rest_schemas.user import UserCreate, UserRead


class StockMapper:
    def __init__(self):
        pass

    @singledispatchmethod
    def to_model(self, data, *args, **kwargs) -> User:
        raise NotImplementedError("지원하지 않는 타입입니다.")

    @singledispatchmethod
    def to_schema(self, data, *args, **kwargs) -> User:
        raise NotImplementedError("지원하지 않는 타입입니다.")

    @to_model.register
    def _(self, stock: StockCreate) -> Stock:
        return Stock(
            name=stock.name,
            current_price=stock.start_price,
            opening_price=stock.start_price,
            closing_price=0,
            volume=stock.volume,
        )
