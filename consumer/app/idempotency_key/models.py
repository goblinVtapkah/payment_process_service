import uuid

from sqlalchemy import Integer, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base

# сущность платежа
class IdempotencyKey(Base):
	__tablename__ = "idempotency_keys"
	# айди
	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
	# имя ключа идемпотентности
	idempotency_key: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), unique=True)