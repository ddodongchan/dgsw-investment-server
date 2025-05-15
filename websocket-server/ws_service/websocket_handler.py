from fastapi import WebSocket

from ws_clients.internal_api_client import request_get_stocks
from ws_schemas.order import Order
from ws_clients.redis_client import get_redis
from ws_util.redis_converter import convert_to_redis_compatible


async def order_stock(websocket: WebSocket):
    await websocket.accept()
    redis = await get_redis()
    while True:
        try:
            data = await websocket.receive_json()
            order = Order(**data)
            order_dict = order.model_dump()
            order_dict["timestamp"] = order.timestamp.isoformat()
            order_dict["type"] = order.type.value
            order_dict["kind"] = order.kind.value
            order_dict = convert_to_redis_compatible(order_dict)
            await redis.xadd("order_stream", order_dict)
            await websocket.send_json({"status": "ok", "message": "Order received"})
        except Exception as e:
            await websocket.send_json({"status": "error", "message": str(e)})

async def get_stocks(websocket: WebSocket):
    stocks = await request_get_stocks()
    await websocket.send_json({
        "type": "stock_info",
        "data": [stock.model_dump() for stock in stocks]
    })