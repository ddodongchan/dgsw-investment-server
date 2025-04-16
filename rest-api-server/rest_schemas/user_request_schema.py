from uuid import UUID

from pydantic import BaseModel

class SaveUserProfileRequest(BaseModel):
    credential_id: UUID
    email: str
    name: str
    profile_image: str