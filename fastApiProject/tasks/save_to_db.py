from sqlalchemy import select, delete
from core.database import AsyncSessionLocal
from models.models import Pairs
import json
from core.logs import log


async def save_to_db(pair, price):
    try:
        async with AsyncSessionLocal() as db:
            pair_in_db = await db.execute(select(Pairs).filter(Pairs.symbol == pair))
            itog = pair_in_db.fetchone()
            if itog is None:
                new_pair = Pairs(symbol=pair, price=price)
                db.add(new_pair)
                await db.commit()
                log.info(f"New pair: {pair} - {price}")
            else:
                await db.execute(delete(Pairs).where(Pairs.symbol == pair))
                new_pair = Pairs(symbol=pair, price=price)
                db.add(new_pair)
                await db.commit()
                log.info(f"Pair: {pair} - {price} updated")
            log.info("db_updated")
    except:
        log.warning(
            f"Pair: {pair} - {float(price)} not to database!"
        )


async def message_handler(msg):
    log.info(f"Message received: {msg}")
    log.info(f"Saving to DB")
    json_data = msg.data.decode()
    data_dict = json.loads(json_data)
    await save_to_db(data_dict["pair"], data_dict["price"])