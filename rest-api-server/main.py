import asyncio
import contextlib
from contextlib import asynccontextmanager

from fastapi import FastAPI

from rest_config.db_session import init_db
from rest_repositories.order_repository import OrderRepository
from rest_repositories.stock_repository import StockRepository
from rest_routers.internal.user_internal_router import user_internal_router
from rest_routers.stock_router import stock_router
from rest_services.order_consumer import OrderConsumer
from rest_services.order_trade_consumer import TradeConsumer

order_repository = OrderRepository()
stock_repository = StockRepository()

order_consumer = OrderConsumer(
    stock_repository=stock_repository,
)
order_trade_consumer = TradeConsumer(
    stock_repository=stock_repository,
    order_repository=order_repository
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    # 여러 백그라운드 태스크 실행
    tasks = [
        asyncio.create_task(order_consumer.consume_orders()),
        asyncio.create_task(order_trade_consumer.consume_matches()),
    ]

    try:
        yield
    finally:
        # 모든 태스크 취소
        for task in tasks:
            task.cancel()
        # 취소 완료 대기
        for task in tasks:
            with contextlib.suppress(asyncio.CancelledError):
                await task

app = FastAPI(lifespan=lifespan)

app.include_router(user_internal_router)
app.include_router(stock_router)

@app.get("/")
async def root():
    return {"message": "Rest API Server is running 🚀"}
