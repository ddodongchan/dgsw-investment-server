from typing import Any, Coroutine

from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from auth_models.user_credentials import UserCredential

class UserCredentialRepository:
    def __init__(self):
        pass

    async def find_by_login_id(self, login_id: str, session: AsyncSession) -> UserCredential | None:
        stmt = select(UserCredential).where(UserCredential.login_id == login_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()