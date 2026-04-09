from datetime import datetime
from decimal import Decimal
import uuid

from sqlalchemy import String, Integer, DateTime, Numeric, Enum, JSON, UUID, func
from sqlalchemy.orm import Mapped, mapped_column

from app.common.enums import Currency, Status
from app.core.db import Base

# сущность платежа
class Payment(Base):
	__tablename__ = "payments"
	# айди
	payment_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
	# сумма
	amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
	# валюта
	currency: Mapped[Currency] = mapped_column(Enum(Currency, name="currency_enum"))
	# описание
	description: Mapped[str] = mapped_column(String)
	# метадата
	meta: Mapped[dict] = mapped_column(JSON)
	# статус
	status: Mapped[Status] = mapped_column(Enum(Status, name="status_enum"))
	# ключ идемпотентности
	idempotency_key: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), unique=True)
	# вебхук для уведомления
	webhook_url: Mapped[str] = mapped_column(String(2048))
	# время создания заявки на платёж
	created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
	# время обработки платежа	
	executed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)