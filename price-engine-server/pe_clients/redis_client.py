# redis_stream.py
import redis.asyncio as redis

from pe_config.setting import settings

# Redis 연결
redis = redis.Redis(host=settings.redis_stream_host, port=settings.redis_stream_port, db=0)
async def get_redis():
    return redis
# Redis Stream 키
ORDER_STREAM = "order_stream"
MATCH_STREAM = "match_stream"
TRADE_STREAM = "trade_stream"