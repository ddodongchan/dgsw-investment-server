from datetime import datetime, timedelta
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from rest_models.news import News


class NewsRepository:
    def __init__(self):
        pass

    async def find_by_news_id(self, news_id: UUID, db_session: AsyncSession):
        stmt = select(News).options(selectinload(News.user)).where(News.id == news_id)
        result = await db_session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_all_with_count(
        self,
        db_session: AsyncSession,
        page: int = 1,
        page_size: int = 10
    ):
        offset = (page - 1) * page_size

        stmt = (select(News).options(
            selectinload(News.user),
            selectinload(News.stock)
        ).offset(offset).limit(page_size))
        result = await db_session.execute(stmt)
        news_list = result.scalars().all()

        return news_list

    async def find_by_date(self, stock_id: UUID, days: int, db_session: AsyncSession):
        from_date = datetime.now() - timedelta(days=days)
        now = datetime.now()

        stmt = (
            select(News).options(
                selectinload(News.user),
                selectinload(News.stock)
            )
            .where(News.stock_id == stock_id)
            .where(News.date >= from_date)
            .where(News.date <= now)
            .order_by(News.id.desc())
            .limit(10)
        )

        result = await db_session.execute(stmt)
        return result.scalars().all()
