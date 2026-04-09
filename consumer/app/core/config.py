import os

class Settings:
	DATABASE_URL = os.getenv("DATABASE_URL")
	ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL")
	RABBITMQ_URL = os.getenv("RABBITMQ_URL")

settings = Settings()