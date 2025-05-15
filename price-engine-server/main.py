import asyncio
import contextlib
from contextlib import asynccontextmanager

from fastapi import FastAPI

from pe_service.match_consumer import OrderConsumer

order_consumer = OrderConsumer()
@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(order_consumer.consume_matches())
    try:
        yield
    finally:
        task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await task

app = FastAPI(lifespan = lifespan)

@app.get("/")
async def root():
    return {"message": "Rest API Server is running 🚀"}
