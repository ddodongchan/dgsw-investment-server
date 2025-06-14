from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class NewsResponse(BaseModel):
    user_id: UUID
    user_name: str
    stock_id: UUID
    stock_name: str
    title: str
    context: str
    date: datetime
    read: int