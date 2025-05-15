from sqlalchemy.ext.asyncio import AsyncSession

from rest_mapper.stock_mapper import StockMapper
from rest_models.stock import Stock
from rest_repositories.stock_repository import StockRepository
from rest_schemas.stock import StockCreate


class StockService:
    def __init__(self, stock_mapper: StockMapper, stock_repository: StockRepository):
        self.stock_mapper = stock_mapper
        self.stock_repository = stock_repository

    async def ipo_stock(self, stock: StockCreate, db_session: AsyncSession):
        db_session.add(self.stock_mapper.to_model(stock))

    async def get_stock(self, db_session: AsyncSession) -> list[Stock]:
        stocks: list[Stock] = await self.stock_repository.find_all(db_session)
        return stocks