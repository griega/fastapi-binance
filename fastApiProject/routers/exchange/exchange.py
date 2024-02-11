import aioredis
import fastapi as fa
from sqlalchemy import orm
import typing
from p_models.cources import Courses
from core import cache
from core.database import get_db
from routers.exchange import helper as exchange_helper
from routers.exchange import tasks as exchange_task

exchange_router_v1 = fa.APIRouter()


@exchange_router_v1.get(
    "/exchange", response_model=Courses, summary="Get symbol info (Version 1)"
)
async def get_symbol_info_v1(
    symbol: typing.Optional[str] = "",
    redis_conn: aioredis.Redis = fa.Depends(cache.connect_redis),
    db: orm.Session = fa.Depends(get_db),
) -> typing.Dict[str, typing.Any]:
    exchanger_name = await cache.get_exchanger_name()
    data = {"exchange": str(exchanger_name)}

    courses = await exchange_helper.get_info_from_cache(redis_conn, symbol)

    if not courses:
        courses = await exchange_helper.storing_info_in_cache(symbol, db)
        if courses:
            await exchange_task.cache_data_in_background(redis_conn, courses)

    data["courses"] = courses
    return data