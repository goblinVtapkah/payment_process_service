from pydantic import BaseModel, HttpUrl

import uuid
from datetime import datetime
from decimal import Decimal

from app.common.enums import Currency, Status

# схема ожидаеммых данных при создании платежа
class PaymentCreate(BaseModel):
	# сумма
	amount: Decimal
	# валюта
	currency: Currency
	# описание
	description: str
	# метаданные
	meta: dict
	# вебхук для уведомления
	webhook_url: HttpUrl

# схема возращаемых данных платежа после создания
class PaymentCreateResponse(BaseModel):
	# айди платежа
	payment_id: int
	# статус
	status: Status
	# время создания
	created_at: datetime

	model_config = {"from_attributes": True}

# схема детальных данных платежа
class PaymentRead(BaseModel):
	# айди
	payment_id: int
	# сумма
	amount: Decimal
	# валюта
	currency: Currency
	# описание
	description: str
	# метадата
	meta: dict
	# статус
	status: Status
	# ключ идемпотентности
	idempotency_key: uuid.UUID
	# вебхук для уведомления
	webhook_url: str
	# время создания заявки на платёж
	created_at: datetime
	# время обработки платежа	
	executed_at: datetime | None

	model_config = {"from_attributes": True}

# схема ожидаеммых данных при обновлении статуса
class PaymentUpdateStatus(BaseModel):
	# айди платежа
	payment_id: int
	# статус платежа
	status: Status