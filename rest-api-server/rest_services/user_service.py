from sqlalchemy.ext.asyncio import AsyncSession

from rest_mapper.user_mapper import UserMapper
from rest_schemas.user_request_schema import SaveUserProfileRequest


class UserService:
    def __init__(self):
        pass

    async def save_user_profile(self, request: SaveUserProfileRequest, db_session: AsyncSession):
        db_session.add(UserMapper.to_model(request))

