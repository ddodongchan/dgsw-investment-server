from rest_mapper.stock_mapper import StockMapper
from rest_repositories.stock_repository import StockRepository
from rest_services.stock_service import StockService


class StockServiceDepends:
    def __init__(self):
        self.stock_mapper = StockMapper()
        self.stock_repository = StockRepository()

    def __call__(self) -> StockService:
        return StockService(
            stock_mapper=self.stock_mapper,
            stock_repository=self.stock_repository,
        )
