from pydantic_settings import BaseSettings

class Settings(BaseSettings):
	DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@postgres:5432/payment_service_db"
	RABBITMQ_URL: str = "amqp://rabbit:rabbitPassword@rabbitmq:5672/"
	FASTAPI_PORT: int = 8000

	class Config:
		env_file = "./.env"

settings = Settings()