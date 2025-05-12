from typing import List
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from rest_mapper.news_mapper import NewsMapper
from rest_models.news import News
from rest_repositories.news_repository import NewsRepository
from rest_repositories.user_repository import UserRepository
from rest_schemas.news_request_schema import SaveNewsRequest, UpdateNewsRequest
from rest_schemas.news_response_schema import NewsResponse
from rest_schemas.user_schema import UserSession


class NewsService:
    def __init__(self, user_repository: UserRepository, news_repository: NewsRepository, news_mapper: NewsMapper):
        self.user_repository = user_repository
        self.news_repository = news_repository
        self.news_mapper = news_mapper

    async def add_news(self, request:SaveNewsRequest, db_session: AsyncSession, user_session: UserSession):
        user_id = user_session.user_id
        user = await self.user_repository.find_by_user_id(
            user_id=user_id,
            db_session=db_session
        )
        db_session.add(self.news_mapper.to_model_save(
            request = request,
            user_id = user_id
        )
        )

    async def find_news_by_id(self, news_id: UUID, db_session: AsyncSession) -> NewsResponse:
        news: News = await self.news_repository.find_by_news_id(
            news_id=news_id,
            db_session=db_session
        )
        news.read += 1
        db_session.add(news)
        return self.news_mapper.to_schema(news)

    async def find_all_news(self, db_session: AsyncSession, page: int, size: int) -> List[NewsResponse]:
        list = await self.news_repository.find_all_with_count(
            db_session=db_session,
            page=page,
            page_size=size
        )
        return [self.news_mapper.to_schema(news = news,) for news in list]

    async def update_news(self, db_session: AsyncSession, request:UpdateNewsRequest, user_session: UserSession):
        news = await self.news_repository.find_by_news_id(request.news_id, db_session=db_session)
        if news.user_id != user_session.user_id:
            raise HTTPException(status_code=403, detail="cannot access")
        news.title = request.title
        news.context = request.context