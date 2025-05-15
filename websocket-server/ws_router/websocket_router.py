from fastapi import WebSocket, APIRouter
from ws_service.websocket_handler import order_stock

websocket_router = APIRouter(
    prefix="/stock",
    tags=["WebSocket"],
)

@websocket_router.websocket("/order")
async def websocket_endpoint(websocket: WebSocket):
    await order_stock(websocket)
