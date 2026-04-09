from app.idempotency_key import crud
from requests import put, post

from random import randint
from time import sleep
import uuid

# эмуляция рабочего сервиса с 3 ретраями (на коленке накинуто)
def emulate_payment_service():
	for _ in range(3):
		sleep(randint(2,5))
		if randint(0,9): return True
	return False

class IdempotencyKeyService:
	@staticmethod
	def create_idempotency_key(session, payment: dict):
		idempotency_key = payment["idempotency_key"]
		existing = IdempotencyKeyService.check_idempotency_key(session, idempotency_key)
		if existing:
			return False
		
		crud.create_idempotency_key(session, idempotency_key)

		status = "successed" if emulate_payment_service() else "failed"

		result = put("http://api:8000/api/v1/payments/status", json={"payment_id": payment["payment_id"], "status": status}).text
		try:
			post(payment["webhook_url"], data=result)
		except Exception as error:
			print(error)

		return True

	@staticmethod
	def check_idempotency_key(session, idempotency_key: uuid.UUID):
		result = crud.get_idempotency_key(session, idempotency_key)
		return True if result else False