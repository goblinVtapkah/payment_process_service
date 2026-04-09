import enum

class Status(enum.Enum):
	PENDING = "pending"
	SUCCESSED = "successed"
	FAILED = "failed"

class Currency(enum.Enum):
	RUB = "RUB"
	USD = "USD"
	EUR = "EUR"