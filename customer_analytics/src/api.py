from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
import pandas as pd
import joblib
import time

from logger import setup_logger

logger = setup_logger()

# Глобальні змінні для зберігання моделей у пам'яті
processor = None
classifier = None
clusterer = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Життєвий цикл додатку: виконується під час запуску сервера."""
    global processor, classifier, clusterer
    try:
        processor = joblib.load('../models/processor.joblib')
        classifier = joblib.load('../models/classifier.joblib')
        clusterer = joblib.load('../models/clusterer.joblib')
        logger.info("Моделі завантажено", extra={"extra_info": {"status": "startup_success"}})
    except Exception as e:
        logger.error("Помилка ініціалізації", extra={"extra_info": {"error": str(e)}})
        raise RuntimeError(f"Не вдалося завантажити моделі: {e}")

    yield  # Тут сервер працює та приймає запити
    # Сюди можна додати логіку очищення пам'яті під час вимкнення сервера


app = FastAPI(title="Customer Analytics API", lifespan=lifespan)


class CustomerRequest(BaseModel):
    """Схема очікуваних даних (сувора типізація)."""
    age: float
    tenure: float
    balance: float
    num_products: int


@app.post("/predict")
async def predict(customer: CustomerRequest):
    start_time = time.time()
    try:
        # 1. Трансформація вхідного JSON (моделі Pydantic) у pandas DataFrame
        df = pd.DataFrame([customer.model_dump()])

        # 2. Попередня обробка даних (нашим скейлером з ml_pipeline.py)
        X_processed = processor.transform(df)

        # 3. Інференс (predict)
        churn_prob = classifier.predict_proba(X_processed)[0][1]  # Ймовірність класу 1
        segment = int(clusterer.predict(X_processed)[0])

        # 4. Формування відповіді
        response_data = {
            "churn_probability": round(float(churn_prob), 4),
            "will_churn": bool(churn_prob > 0.5),
            "customer_segment": segment
        }

        # 5. Observability: записуємо все у структурований лог
        process_time = round(time.time() - start_time, 4)
        logger.info("Прогноз успішно згенеровано", extra={
            "extra_info": {
                "request_data": customer.model_dump(),
                "response": response_data,
                "process_time_sec": process_time
            }
        })

        return response_data

    except Exception as e:
        logger.error("Помилка обробки запиту", extra={"extra_info": {"error": str(e)}})
        raise HTTPException(status_code=500, detail="Внутрішня помилка сервера")