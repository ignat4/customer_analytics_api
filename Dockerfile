FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY customer_analytics/models/ ./models/
COPY customer_analytics/src/ ./src/

WORKDIR /app/src

# Відкриваємо порт 8000
EXPOSE 8000

# Команда запуску сервера
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]