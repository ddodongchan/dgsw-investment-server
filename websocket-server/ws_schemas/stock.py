from pydantic import BaseModel

class Stock(BaseModel):
    id: int
    name: str
    current_price: float
    opening_price: float
    closing_price: float
    volume: int