# образ Python
FROM python:3.12-slim

# обновляем apt-get
RUN apt-get update

# устанавливаем зависимости для postgres и rabbitmq
RUN apt-get install -y \
    build-essential \
    libpq-dev

# чистим кеш
RUN rm -rf /var/lib/apt/lists/*

# настраиваем рабочую директорию
WORKDIR /app

# перекидываем python зависимости(библиотеки)
COPY requirements.txt .

# скачиваем и устанавливаем библиотеки из requirements
RUN pip install --no-cache-dir -r requirements.txt

# перекидывваем код и данные миграций
COPY ./app ./app
COPY ./alembic ./alembic

# переменные окружения для python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
	PYTHONPATH=/app

# перекидываем алембик ини
COPY alembic.ini .

# копируем entrypoint
COPY entrypoint.sh /entrypoint.sh

# настраиваем права доступа
RUN chmod +x /entrypoint.sh

# запускаем entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# запускаем fastapi через uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]