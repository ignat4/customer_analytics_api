# Використовуємо офіційний легкий образ Python
FROM python:3.12-slim

# Встановлюємо робочу директорію всередині контейнера
WORKDIR /app

# Копіюємо файл із залежностями та встановлюємо їх
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ОНОВЛЕНІ РЯДКИ: вказуємо Docker, що папки лежать усередині customer_analytics
COPY customer_analytics/models/ ./models/
COPY customer_analytics/src/ ./src/

# Переходимо в папку src (Python-код очікує запуск звідси)
WORKDIR /app/src

# Відкриваємо порт 8000
EXPOSE 8000

# Команда запуску сервера
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]