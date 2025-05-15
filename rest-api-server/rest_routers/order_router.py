from fastapi import APIRouter

from rest_clients.redis_client import redis, ORDER_STREAM
from rest_schemas.order import OrderCreate

stock_router = APIRouter(
    prefix="/stocks",
    tags=["order"]
)
@stock_router.post("/orders")
async def create_order(order: OrderCreate):
    await redis.xadd(ORDER_STREAM, order.model_dump())
    return {"status": "queued"}