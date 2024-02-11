import uvicorn
import asyncio
from aiomultiprocess import Process
from services.ws_bin import update_info
from fastapi import FastAPI
from routers.exchange.exchange import exchange_router_v1

app = FastAPI()
app.include_router(exchange_router_v1, prefix="/api/v1", tags=["exchange"])


async def run_app():
    await uvicorn.run("main:app", host="0.0.0.0", port=9999, reload=True, workers=10)


async def tasks_run():
    uvicorn_process = Process(target=run_app)
    uvicorn_process.start()

    await update_info()

    uvicorn_process.join()


if __name__ == "__main__":
    asyncio.run(tasks_run())