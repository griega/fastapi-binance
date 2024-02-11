import aioredis
import typing
import json


async def cache_data_in_background(
    redis_conn: aioredis.Redis, courses: typing.List[typing.Dict[str, typing.Any]]
):
    for course in courses:
        await redis_conn.set(course["direction"], json.dumps(course["value"]))