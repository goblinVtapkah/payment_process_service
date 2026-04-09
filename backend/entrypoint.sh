#!/bin/bash
# entrypoint.sh

# применяем миграции
alembic upgrade head

# запускаем приложение
exec "$@"