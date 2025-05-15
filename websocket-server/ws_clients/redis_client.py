import redis.asyncio as redis

from ws_config.setting import settings

redis_client = redis.Redis(
    host=settings.redis_stream_host,
    port=settings.redis_stream_port,
    db=0,
    decode_responses=True
)

async def get_redis():
    return redis_client