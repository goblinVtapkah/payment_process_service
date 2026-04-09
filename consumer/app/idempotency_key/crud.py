from sqlalchemy.orm import Session
from sqlalchemy import select

from app.idempotency_key.models import IdempotencyKey

import uuid

def create_idempotency_key(session: Session, idempotency_key: uuid.UUID) -> IdempotencyKey:
	idempotency_key = IdempotencyKey(idempotency_key=idempotency_key)
	session.add(idempotency_key)
	session.commit()
	session.refresh(idempotency_key)
	return idempotency_key

def get_idempotency_key(session: Session, idempotency_key: uuid.UUID) -> IdempotencyKey | None:
	return session.execute(select(IdempotencyKey).where(IdempotencyKey.idempotency_key == idempotency_key)).scalar_one_or_none()