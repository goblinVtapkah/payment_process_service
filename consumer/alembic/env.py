import asyncio

from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

from app.core.config import settings

from app.core.db import Base
from app.idempotency_key.models import *

# конфиг алембика
config = context.config

# сохраняем логи
fileConfig(config.config_file_name)

# получаем модели
target_metadata = Base.metadata

# миграции, если бд не запущена
def run_migrations_offline():
	url = settings.ASYNC_DATABASE_URL
	context.configure(
		url=url,
		target_metadata=target_metadata,
		literal_binds=True,
		dialect_opts={"paramstyle": "named"},
		version_table="consumer_alembic_version",
	)
	with context.begin_transaction():
		context.run_migrations()


# миграции, если бд запущена
async def run_migrations_online():
	connectable = create_async_engine(settings.ASYNC_DATABASE_URL)

	async with connectable.connect() as connection:
		await connection.run_sync(do_run_migrations)

	await connectable.dispose()

def do_run_migrations(sync_connection):
    context.configure(
        connection=sync_connection,
        target_metadata=target_metadata,
		version_table="consumer_alembic_version",
    )

    with context.begin_transaction():
        context.run_migrations()

# запускаем нужный режим миграции
if context.is_offline_mode():
	run_migrations_offline()
else:
	asyncio.run(run_migrations_online())