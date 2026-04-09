from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.payments import crud
from app.payments.schemas import PaymentCreate, PaymentRead, PaymentUpdateStatus
from app.payments.tasks import publish_payment_created

import uuid

class PaymentService:

	@staticmethod
	async def create_payment(session: AsyncSession, data: PaymentCreate, idempotency_key: uuid.UUID):
		existing = await crud.get_payment_by_idempotency_key(session, idempotency_key)
		if existing:
			return existing

		payment = await crud.create_payment(session, data, idempotency_key)

		if not payment:
			raise HTTPException(status_code=400, detail="Idempotency Key alredy exists")

		await publish_payment_created(PaymentRead.from_orm(payment))

		return payment

	@staticmethod
	async def get_payment(session: AsyncSession, payment_id: int):
		payment = await crud.get_payment(session, payment_id)
		if not payment:
			raise HTTPException(status_code=404, detail="Payment not found")
		return payment

	@staticmethod
	async def update_status(session: AsyncSession, data: PaymentUpdateStatus):
		return await crud.update_payment_status(session, data)