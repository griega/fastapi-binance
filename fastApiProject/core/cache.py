import aioredis
from config import settings
import json
from core.logs import log

async def connect_redis()->aioredis.Redis:
    redis_db = await aioredis.from_url(
        f"redis://{settings.redis_host}:{settings.redis_port}/1",
        encoding = "utf8",
    )
    return redis_db

async def close_redis(redis: aioredis.Redis) -> None:
    await redis.close()


async def set_value(symbol: str, value: float) -> None:
    redis = await connect_redis()
    try:
        await redis.set(symbol, value)
    finally:
        log.info(f"Saved in cache is true: {symbol} - {value}")
        await close_redis(redis)


async def get_exchanger_name() -> str:
    redis = await connect_redis()
    exchanger_name = await redis.get("exchanger")
    return exchanger_name.decode("utf-8")


async def get_value(symbol: str) -> float:
    redis = await connect_redis()
    try:
        price = await redis.get(symbol)
        return float(price) if price is not None else 0.0
    finally:
        await close_redis(redis)


async def message_handler(msg):
    log.info(f"message received: {msg}")
    log.info(f"Saving to cache")
    json_data = msg.data.decode()
    data_dict = json.loads(json_data)
    await set_value(data_dict["pair"], data_dict["price"])