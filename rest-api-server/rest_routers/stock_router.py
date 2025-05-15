from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from rest_config.db_session import get_db_session
from rest_depends.stock_depends import StockServiceDepends
from rest_schemas.stock import StockCreate
from rest_services.stock_service import StockService

stock_router = APIRouter(
    prefix="/stocks",
    tags=["stock"]
)

@stock_router.post("/")
async def ipo_stock(
        stock: StockCreate,
        stock_service: StockService = Depends(StockServiceDepends()),
        db_session: AsyncSession = Depends(get_db_session),
):
    return await stock_service.ipo_stock(stock, db_session)