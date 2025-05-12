from fastapi import Header, HTTPException
from uuid import UUID

from rest_schemas.user_schema import UserSession


async def get_user_session(
    user_id: UUID = Header(..., alias="X-User-ID"),
    role: str = Header(..., alias="X-User-Role")
):
    if not user_id or not role:
        raise HTTPException(status_code=400, detail="Missing user ID or role")

    return UserSession(
        user_id=user_id,
        role=role
    )