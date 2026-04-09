from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from app.payments.models import Payment
from app.payments.schemas import PaymentCreate, PaymentUpdateStatus
from app.common.enums import Status

import uuid

async def create_payment(session: AsyncSession, data: PaymentCreate, idempotency_key: uuid.UUID) -> Payment:
	payment = Payment(**data.model_dump(mode="json"), idempotency_key=idempotency_key, status=Status.PENDING)
	session.add(payment)
	try:
		await session.commit()
		await session.refresh(payment)
	except:
		await session.rollback()
		return
	return payment

async def update_payment_status(session: AsyncSession, data: PaymentUpdateStatus) -> Payment:
	payment = await session.get(Payment, data.payment_id)
	if payment:
		payment.status = data.status
		payment.executed_at = datetime.now()
		await session.commit()
		await session.refresh(payment)
	return payment

async def get_payment_by_idempotency_key(session: AsyncSession, idempotency_key: uuid.UUID) -> Payment | None:
	return (await session.execute(select(Payment).where(Payment.idempotency_key == idempotency_key))).scalar_one_or_none()

async def get_payment(session: AsyncSession, payment_id: int) -> Payment | None:
	return await session.get(Payment, payment_id)