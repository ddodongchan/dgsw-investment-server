from fastapi import APIRouter, Depends

from rest_config.db_session import get_db_session
from rest_depends.internal_auth_middleware import verify_internal_api_key
from rest_depends.stock_depends import StockServiceDepends
from rest_models.stock import Stock
from rest_schemas.stock import StockCreate

stock_internal_router = APIRouter(
    prefix="/internal/stocks",
    tags=["stock"],
    dependencies=[Depends(verify_internal_api_key)]
)

@stock_internal_router.get("/")
async def get_stocks(
        stock: StockCreate,
        stock_service: Depends(StockServiceDepends),
        db_session: Depends(get_db_session),
) -> list[Stock]:
    return await stock_service.get_stock(stock, db_session)