# redis_stream.py
import redis.asyncio as redis

# Redis 연결
redis = redis.Redis(host='localhost', port=6379, db=0)
async def get_redis():
    return redis
# Redis Stream 키
ORDER_STREAM = "order_stream"
MATCH_STREAM = "match-stream"