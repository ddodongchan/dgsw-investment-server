from uuid import UUID

from rest_clients.redis_client import get_redis, ORDER_STREAM, MATCH_STREAM
from rest_config.db_session import get_db_session_for_consumer
from rest_enum.order_enum import OrderStatus, OrderKind, OrderType
from rest_models.order import Order
from rest_repositories.stock_repository import StockRepository


class OrderConsumer:
    def __init__(self, stock_repository: StockRepository,):
        self.stock_repository = stock_repository

    # Redis Stream Consumer (백그라운드 태스크)
    async def consume_orders(self):
        redis = await get_redis()
        group = "api_group"
        consumer = "api_consumer"
        try:
            await redis.xgroup_create(name=ORDER_STREAM, groupname=group, id="0-0", mkstream=True)
        except Exception:
            pass

        while True:
            resp = await redis.xreadgroup(group, consumer, streams={ORDER_STREAM: '>'}, count=10, block=5000)
            for stream_name, messages in resp:
                for msg_id, data in messages:
                    await self.process_order(data = data)
                    await redis.xack(ORDER_STREAM, group, msg_id)
                    await redis.xadd(MATCH_STREAM, data)

    # 실제 주문 처리 로직 (DB 저장)
    async def process_order(self, data: dict):
        if isinstance(next(iter(data.keys())), bytes):
            data = {k.decode(): v.decode() for k, v in data.items()}
        try:
            async with get_db_session_for_consumer() as session:
                stock_id = data["stock_id"]
                exists_stock = await self.stock_repository.exists_by_id(stock_id, session)
                if not exists_stock: raise Exception(f"stock_id {stock_id} does not exist")
                order = Order(
                    id= UUID(data['order_id']),
                    user_id=UUID(data["user_id"]),
                    stock_id=stock_id,
                    type=OrderType(data["type"]),
                    status=OrderStatus.PENDING,
                    amount=int(data["amount"]),
                    price=float(data["price"]),
                    kind=OrderKind(data["kind"]),
                    filled=0,
                )
                session.add(order)
                await session.commit()
        except Exception as e:
            print("Order 저장 실패:", e)
            raise