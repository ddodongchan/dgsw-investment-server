from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from rest_models.user import User


class UserRepository:
    def __init__(self):
        pass

    async def find_by_login_id(self, login_id: str, db_session: AsyncSession):
        stmt = select(User).where(User.login_id == login_id)
        result = await db_session.execute(stmt)
        return result.scalar_one_or_none()

    async def exists_by_id(self, user_id: int, db_session: AsyncSession) -> bool:
        stmt = select(
            exists().where(User.id == user_id)
        )
        result = await db_session.execute(stmt)
        return result.scalar()