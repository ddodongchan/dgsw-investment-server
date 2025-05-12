from uuid import UUID

from pydantic import BaseModel


class UserSession(BaseModel):
    user_id: UUID
    role: str