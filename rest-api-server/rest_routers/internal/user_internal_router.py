from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from rest_config.db_session import get_db_session
from rest_depends.internal_auth_middleware import verify_internal_api_key
from rest_depends.user_depends import UserServiceDepends
from rest_schemas.user import UserRead, UserCreate
from rest_services.user_service import UserService

user_internal_router = APIRouter(
    prefix="/internal/users",
    tags=["InternalUser"],
    dependencies=[Depends(verify_internal_api_key)]
)

@user_internal_router.post("/", response_model=UserRead)
async def save_user(
        request: UserCreate,
        db: AsyncSession = Depends(get_db_session),
        user_service: UserService = Depends(UserServiceDepends())
) -> UserRead:
    return await user_service.save_user(request, db)

@user_internal_router.get("/", response_model=UserRead)
async def get_user_by_login_id(
        login_id: str,
        db: AsyncSession = Depends(get_db_session),
        user_service: UserService = Depends(UserServiceDepends())
) -> UserRead:
    return await user_service.get_user_by_login_id(login_id, db)