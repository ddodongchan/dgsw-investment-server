from uuid import UUID

from rest_mapper.news_mapper import NewsMapper
from rest_repositories.news_repository import NewsRepository
from rest_repositories.stock_repository import StockRepository


class PeService:
    def __init__(self, stock_repository: StockRepository, news_repository: NewsRepository):
        self.stock_repository = StockRepository
        self.news_repository = news_repository

    def calculate_price(self, stock_id: UUID):
        stock = self.stock_repository.find_by_id(stock_id)
