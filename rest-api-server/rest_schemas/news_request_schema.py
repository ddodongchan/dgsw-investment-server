from uuid import UUID

from pydantic import BaseModel


class SaveNewsRequest(BaseModel):
    title: str
    context: str
    stock_id: UUID

class UpdateNewsRequest(BaseModel):
    news_id: UUID
    title: str
    context: str