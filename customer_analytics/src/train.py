import pandas as pd
import numpy as np
import os
from ml_pipeline import CustomerDataProcessor, CustomerModels


def generate_mock_data(n_samples: int = 1000) -> pd.DataFrame:
    """Генерує синтетичні дані для тренування, щоб не шукати датасет."""
    np.random.seed(42)
    data = {
        'age': np.random.normal(40, 12, n_samples),
        'tenure': np.random.randint(0, 10, n_samples),
        'balance': np.random.normal(50000, 20000, n_samples),
        'num_products': np.random.randint(1, 4, n_samples),
        # Штучно створюємо залежність для таргета (churn)
        'churn': np.random.choice([0, 1], n_samples, p=[0.8, 0.2])
    }
    # Додаємо трохи логіки: старші клієнти з меншим балансом ідуть частіше
    df = pd.DataFrame(data)
    df.loc[(df['age'] > 50) & (df['balance'] < 40000), 'churn'] = 1
    return df


def main():
    # 1. Створюємо директорію для моделей, якщо її немає
    os.makedirs('../models', exist_ok=True)

    # 2. Отримуємо дані
    print("Завантаження даних...")
    df = generate_mock_data()
    y = df['churn']

    # 3. Ініціалізуємо та запускаємо процесор даних
    processor = CustomerDataProcessor()
    X_processed = processor.fit_transform(df)

    # 4. Ініціалізуємо та навчаємо моделі
    models = CustomerModels()
    models.train(X_processed, y)

    # 5. Зберігаємо артефакти для API
    print("Збереження моделей у папку /models...")
    processor.save_processor()
    models.save_models()
    print("Навчання завершено успішно!")


if __name__ == "__main__":
    main()