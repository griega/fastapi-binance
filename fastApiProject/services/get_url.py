import aiohttp
import json
from config import settings
from core import cache
from core.logs import log


async def get_rub_exchange_rate():
    url = "https://www.cbr-xml-daily.ru/daily_json.js"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.text()
                try:
                    json_data = json.loads(data)
                    usd_exchange_rate = json_data["Valute"]["USD"]["Value"]
                    return usd_exchange_rate
                except json.JSONDecodeError as e:
                    log.error("Failed to decode JSON data: {e}")
            else:
                log.error(
                    f"Failed to fetch exchange rate data. Status code: {response.status}"
                )


async def get_data_from_coingeko():
    for pair in settings.coin_pairs:
        pair_convert_data = settings.convert_pairs_to_CG_syntax[pair]
        ids, vs_currencies = (
            settings.convert_pairs_to_CG_syntax["id"],
            pair_convert_data["vs_currencies"],
        )
        params = {
            "ids": ids,
            "vs_currencies": vs_currencies,
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    settings.coingecko_url, params=params
                ) as response:
                    if response.status == 200:
                        data = await response.text()
                        try:
                            json_data = json.loads(data)
                            await cache.set_value("exchanger", "coingeko")
                            return {
                                "pair": pair,
                                "price": float(json_data[ids][vs_currencies]),
                            }
                        except json.JSONDecodeError as e:
                            log.warning(e)
            except aiohttp.ClientResponseError as e:
                log.error(f"Error parsing coingeko: {e}")