from uuid import UUID

from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from rest_models.stock import Stock


class StockRepository:
    def __init__(self):
        pass

    async def find_all(self, db_session: AsyncSession) -> list[Stock]:
        stmt = select(Stock)
        result = await db_session.execute(stmt)
        return list(result.scalars().all())

    async def find_by_id(self, stock_id: UUID, db_session: AsyncSession) -> Stock:
        stmt = select(Stock).where(Stock.id == stock_id)
        result = await db_session.execute(stmt)
        return result.scalar_one_or_none()

    async def exists_by_id(self, stock_id: UUID, db_session: AsyncSession) -> bool:
        stmt = select(
            exists().where(Stock.id == stock_id)
        )
        result = await db_session.execute(stmt)
        return result.scalar()