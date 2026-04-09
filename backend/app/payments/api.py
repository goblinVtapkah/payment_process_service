from fastapi import APIRouter, Header, Response, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.payments.schemas import PaymentCreate, PaymentCreateResponse, PaymentRead, PaymentUpdateStatus
from app.core.db import get_session
from app.payments.service import PaymentService

import uuid


router = APIRouter(prefix="/payments", tags=["payments"])

# создать платежа POST /api/v1/payments/
@router.post(
	"/",
	response_model=PaymentCreateResponse,
	status_code=status.HTTP_202_ACCEPTED,
)
async def create(
	response: Response,
	data: PaymentCreate,
	idempotency_key: uuid.UUID = Header(..., alias="Idempotency-Key"),
	session: AsyncSession = Depends(get_session),
):
	response.status_code = status.HTTP_202_ACCEPTED
	return await PaymentService.create_payment(session, data, idempotency_key)

# получить платеж GET /api/v1/payments/{payment_id}
@router.get("/{payment_id}", response_model=PaymentRead)
async def get(payment_id: int, session: AsyncSession = Depends(get_session)):
	return await PaymentService.get_payment(session, payment_id)

# изменить статус платежа PUT /api/v1/payments/status
@router.put("/status", response_model=PaymentRead)
async def update_status(
	data: PaymentUpdateStatus,
	session: AsyncSession = Depends(get_session),
):
	return await PaymentService.update_status(session, data)
