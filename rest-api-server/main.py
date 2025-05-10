import asyncio
import contextlib
from contextlib import asynccontextmanager

from fastapi import FastAPI

from rest_config.db_session import init_db
from rest_routers.internal.user_internal_router import user_internal_router
from rest_routers.stock_router import stock_router
from rest_services.order_consumer import OrderConsumer

order_consumer = OrderConsumer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    task = asyncio.create_task(order_consumer.consume_orders())
    try:
        yield
    finally:
        task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await task

app = FastAPI(lifespan = lifespan)

app.include_router(user_internal_router)
app.include_router(stock_router)

@app.get("/")
async def root():
    return {"message": "Rest API Server is running 🚀"}
