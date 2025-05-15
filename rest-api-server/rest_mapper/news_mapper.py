from uuid import UUID

from rest_models.news import News
from rest_schemas.news_request_schema import SaveNewsRequest, UpdateNewsRequest
from rest_schemas.news_response_schema import NewsResponse


class NewsMapper:
    def to_model_save(self, request: SaveNewsRequest, user_id: UUID) -> News:
        return News(
            user_id=user_id,
            title=request.title,
            read=0,
            context= request.context
        )

    def to_schema(self, news:News) -> NewsResponse:
        return NewsResponse(
            user_id=news.user_id,
            user_name = news.user.name,
            title=news.title,
            context=news.context,
            date=news.date,
            read=news.read,
        )