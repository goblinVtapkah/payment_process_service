import asyncio
from concurrent.futures import ThreadPoolExecutor
from app.core.broker import broker
from app.core.db import SessionLocal
from app.idempotency_key.service import IdempotencyKeyService

executor = ThreadPoolExecutor(max_workers=1)

@broker.subscriber("payments.new")
async def handle_idempotancy_key(payment: dict):
	def sync_task():
		with SessionLocal() as session:
			IdempotencyKeyService.create_idempotency_key(session, payment)

	loop = asyncio.get_event_loop()
	await loop.run_in_executor(executor, sync_task)
