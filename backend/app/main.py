from fastapi import FastAPI
from app.payments.api import router as payment_router
from app.core.broker import broker
import asyncio

API_PREFIX = '/api/v1'

app = FastAPI()
app.include_router(payment_router, prefix=API_PREFIX)

@app.on_event("startup")
async def startup():
    for _ in range(10):
        try:
            await broker.start()
            return
        except Exception:
            await asyncio.sleep(3)

    raise RuntimeError("Broker not available")


@app.on_event("shutdown")
async def shutdown():
    await broker.close()