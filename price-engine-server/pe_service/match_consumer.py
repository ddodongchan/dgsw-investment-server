import json
from datetime import datetime
from uuid import UUID

from pe_clients.redis_client import get_redis, MATCH_STREAM, TRADE_STREAM
from pe_util.uuid_util import convert_uuid


class OrderConsumer:
    def __init__(self):
        pass

    # Redis Stream Consumer (백그라운드 태스크)
    async def consume_matches(self):
        redis = await get_redis()
        group = "price_engine_group"
        consumer = "price_engine_consumer"
        try:
            await redis.xgroup_create(name=MATCH_STREAM, groupname=group, id="0", mkstream=True)
        except Exception:
            pass

        while True:
            entries = await redis.xreadgroup(group, consumer, streams={MATCH_STREAM: '>'}, count=10, block=5000)
            if not entries: pass
            for stream_name, messages in entries:
                for msg_id, data in messages:
                    decoded_order = {k.decode(): v.decode() for k, v in data.items()}
                    await self.match_order(
                        redis = redis,
                        order = decoded_order
                    )
                    await redis.xack(MATCH_STREAM, group, msg_id)

    # 실제 주문 처리 로직 (DB 저장)
    async def match_order(self, redis, order):
        stock_id = UUID(order["stock_id"])
        order_type = order["type"]
        price = float(order["price"])
        quantity = int(order["amount"])
        user_id = UUID(order["user_id"])
        order_id = UUID(order["order_id"])
        opposite_type = "SELLING" if order_type == "BUYING" else "BUYING"
        orderbook_key = f"{opposite_type}:{stock_id}"
        candidates = await self._get_candidates(
            orderbook_key = orderbook_key,
            price = price,
            redis = redis,
            order_type = order_type,
        )
        decoded_candidates = [
            (k.decode(), v) for k, v in candidates
        ]

        for target_id, target_price in decoded_candidates:
            if quantity <= 0:
                break

            # 수량, 가격 등 실제 target order 조회 필요
            target_order_raw_data = await redis.hgetall(f"order:{target_id}")

            if not target_order_raw_data:
                continue
            target_order_data = {k.decode(): v.decode() for k, v in target_order_raw_data.items()}

            target_quantity = int(target_order_data['quantity'])
            traded_quantity = min(quantity, target_quantity)
            trade_price = int(target_price)
            trade_data = {
                "buy_order_id": order_id if order_type == "buy" else target_id,
                "sell_order_id": target_id if order_type == "buy" else order_id,
                "stock_id": stock_id,
                "price": trade_price,
                "quantity": traded_quantity,
                "timestamp": int(datetime.now().timestamp()),
            }
            await redis.xadd(TRADE_STREAM, {"data": json.dumps(trade_data, default=convert_uuid)})


            # 수량 갱신
            quantity -= traded_quantity
            target_quantity -= traded_quantity

            if target_quantity == 0:
                await redis.zrem(orderbook_key, target_id)
                await redis.delete(f"order:{target_id}")
            else:
                await redis.hset(f"order:{target_id}", "quantity", target_quantity)

        # 남은 수량 OrderBook에 등록
        if quantity > 0:
            try:
                await redis.zadd(f"{order_type}:{stock_id}", {str(order_id): price})
                await redis.hset(f"order:{str(order_id)}", mapping={
                    "user_id": str(user_id),
                    "stock_id": str(stock_id),
                    "type": order_type,
                    "price": price,
                    "quantity": quantity
                })
            except Exception as e:
                print(f" Redis에 주문 저장 실패: {e}")
                raise

    async def _get_candidates(self, order_type, price: float, redis, orderbook_key):
        if order_type == "BUYING":
            if price == 0:  # 시장가 주문
                return await redis.zrangebyscore(orderbook_key, "-inf", "+inf", withscores=True)
            else:  # 지정가 주문
                return await redis.zrangebyscore(orderbook_key, "-inf", price, withscores=True)
        elif order_type == "SELLING":
            if price == 0:  # 시장가 주문
                return await redis.zrevrangebyscore(orderbook_key, "+inf", "-inf", withscores=True)
            else:  # 지정가 주문
                return await redis.zrevrangebyscore(orderbook_key, "+inf", price, withscores=True)
        else:
            raise Exception