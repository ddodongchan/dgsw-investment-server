from sqlalchemy.ext.asyncio import AsyncSession

from rest_mapper.user_mapper import UserMapper
from rest_models.user import User
from rest_repositories.user_repository import UserRepository
from rest_schemas.user import UserCreate, UserRead

class UserService:
    def __init__(self, user_repository: UserRepository, user_mapper: UserMapper):
        self.user_mapper = user_mapper
        self.user_repository = user_repository

    async def save_user(self, request: UserCreate, db_session: AsyncSession) -> UserRead:
        user: User = await self.user_repository.find_by_login_id(request.login_id, db_session)
        if user is None:
            user = self.user_mapper.to_model(request)
            db_session.add(user)
            await db_session.flush()
        return self.user_mapper.to_schema(user)

    async def get_user_by_login_id(self, login_id: str, db_session: AsyncSession) -> UserRead:
        user: User = await self.user_repository.find_by_login_id(login_id, db_session)
        return UserRead.model_validate(user)