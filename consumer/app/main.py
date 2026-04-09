from app.core.broker import broker
from app.idempotency_key.tasks import *

import asyncio

async def main():
	for _ in range(10):
		try:
			await broker.start()
			print("Brocker connectend with Consumer")
			try:
				while True:
					await asyncio.sleep(1)
			except:
				await broker.close()
		except Exception:
			await asyncio.sleep(3)

	raise RuntimeError("Broker not available")

if __name__ == "__main__":
	asyncio.run(main())