import json
from datetime import datetime
from uuid import UUID

from rest_clients.redis_client import get_redis, TRADE_STREAM
from rest_config.db_session import get_db_session_for_consumer
from rest_enum.order_enum import OrderStatus
from rest_models.trade import Trade
from rest_repositories.order_repository import OrderRepository
from rest_repositories.stock_repository import StockRepository


class TradeConsumer:
    def __init__(self, stock_repository: StockRepository, order_repository: OrderRepository):
        self.stock_repository = stock_repository
        self.order_repository = order_repository

    async def consume_matches(self):
        redis = await get_redis()
        group = "api_group"
        consumer = "api_consumer"

        try:
            await redis.xgroup_create(name=TRADE_STREAM, groupname=group, id="0", mkstream=True)
        except Exception:
            pass

        while True:
            entries = await redis.xreadgroup(group, consumer, streams={TRADE_STREAM: '>'}, count=10, block=5000)
            if not entries:
                continue

            for stream_name, messages in entries:
                for msg_id, data in messages:
                    decoded_data = {k.decode(): v.decode() for k, v in data.items()}
                    await self.save_match_to_db(redis, decoded_data, msg_id)

    async def save_match_to_db(self, redis, data, msg_id):
        match_data = json.loads(data["data"])
        async with get_db_session_for_consumer() as session:
            buy_order_id: UUID = match_data["buy_order_id"]
            sell_order_id: UUID = match_data["sell_order_id"]
            quantity: int = match_data["quantity"]
            stock_id: UUID = match_data["stock_id"]
            price: float = match_data["price"]

            trade = Trade(
                buy_order_id=buy_order_id,
                sell_order_id=sell_order_id,
                stock_id=stock_id,
                price=price,
                quantity=quantity,
                timestamp=datetime.fromtimestamp(match_data["timestamp"])
            )
            session.add(trade)

            # 주문 정보 불러오기
            buy_order = await self.order_repository.find_by_id(buy_order_id, session)
            sell_order = await self.order_repository.find_by_id(sell_order_id, session)

            # filled 수량 증가
            buy_order.filled += quantity
            sell_order.filled += quantity

            # 상태 업데이트 (enum 있을 경우 enum 활용)
            if buy_order.filled >= buy_order.amount:
                buy_order.status = OrderStatus.FILLED.value
            else:
                buy_order.status = OrderStatus.PARTIAL.value

            if sell_order.filled >= sell_order.amount:
                sell_order.status = OrderStatus.FILLED.value
            else:
                sell_order.status = OrderStatus.PARTIAL.value

            stock = await self.stock_repository.find_by_id(stock_id, session)
            stock.current_price = price
        # ack 처리
        await redis.xack(TRADE_STREAM, "api_group", msg_id)
