from app.core.broker import broker
from app.payments.schemas import PaymentRead

async def publish_payment_created(payment: PaymentRead):
	await broker.publish(payment, queue="payments.new")