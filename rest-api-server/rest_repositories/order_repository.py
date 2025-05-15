from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from rest_models.order import Order


class OrderRepository:
    def __init__(self):
        pass

    async def find_by_id(self, order_id: UUID, db_session: AsyncSession) -> Order:
        stmt = select(Order).where(Order.id == order_id)
        result = await db_session.execute(stmt)
        return result.scalar_one_or_none()