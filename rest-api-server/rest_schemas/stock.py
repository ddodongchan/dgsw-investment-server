from pydantic import BaseModel

class StockCreate(BaseModel):
    name: str
    volume: int
    start_price: float