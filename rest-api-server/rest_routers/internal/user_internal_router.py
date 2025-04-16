from typing import Annotated

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from rest_config.rest_api_db_session import get_db_session
from rest_depends.internal_auth_middleware import verify_internal_api_key
from rest_depends.user_depends import UserServiceDepends
from rest_schemas.user_request_schema import SaveUserProfileRequest
from rest_services.user_service import UserService

user_internal_router = APIRouter(
    prefix="/internal/users",
    tags=["InternalUser"],
    dependencies=[Depends(verify_internal_api_key)]
)

@user_internal_router.post("/")
async def save_user_profile(
        request: SaveUserProfileRequest,
        db: AsyncSession = Depends(get_db_session),
        user_service: UserService = Depends(UserServiceDepends)
):
    return await user_service.save_user_profile(request, db)