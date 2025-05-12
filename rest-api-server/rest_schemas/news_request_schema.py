from uuid import UUID

from pydantic import BaseModel


class SaveNewsRequest(BaseModel):
    title: str
    context: str

class UpdateNewsRequest(BaseModel):
    news_id: UUID
    title: str
    context: str