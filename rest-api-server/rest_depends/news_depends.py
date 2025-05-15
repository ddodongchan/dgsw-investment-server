from rest_repositories.news_repository import NewsRepository
from rest_mapper.news_mapper import NewsMapper
from rest_repositories.user_repository import UserRepository
from rest_services.news_service import NewsService


class NewsServiceDepends:
    def __init__(self):
        self.user_repo = UserRepository()
        self.news_repo = NewsRepository()
        self.news_mapper = NewsMapper()


    def __call__(self) -> NewsService:
        return NewsService(
            user_repository= self.user_repo,
            news_repository= self.news_repo,
            news_mapper=self.news_mapper)