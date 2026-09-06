import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
import joblib
import os


class CustomerDataProcessor:
    """Клас для попередньої обробки даних клієнтів."""

    def __init__(self):
        self.scaler = StandardScaler()
        self.features = ['age', 'tenure', 'balance', 'num_products']

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Навчає скейлер і трансформує дані ."""
        X = df[self.features].copy()
        # Заповнюємо пропуски медіаною, якщо вони є
        X = X.fillna(X.median())

        # Стандартизація ознак
        scaled_features = self.scaler.fit_transform(X)
        return pd.DataFrame(scaled_features, columns=self.features)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Трансформує нові дані на основі навченого скейлера ."""
        X = df[self.features].copy()
        X = X.fillna(X.median())
        scaled_features = self.scaler.transform(X)
        return pd.DataFrame(scaled_features, columns=self.features)

    def save_processor(self, path: str = '../models/processor.joblib'):
        joblib.dump(self, path)


class CustomerModels:
    """Клас, що інкапсулює моделі класифікації та кластеризації."""

    def __init__(self):
        # RandomForest чудово працює «з коробки» для табличних даних
        self.classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        # K-Means для поділу на 3 сегменти
        self.clusterer = KMeans(n_clusters=3, random_state=42, n_init='auto')

    def train(self, X_train: pd.DataFrame, y_train: pd.Series):
        """Навчання обох моделей."""
        print("Навчання моделі передбачення відтоку (RandomForest)...")
        self.classifier.fit(X_train, y_train)

        print("Навчання моделі сегментації (K-Means)...")
        self.clusterer.fit(X_train)

    def save_models(self, clf_path: str = '../models/classifier.joblib',
                    clust_path: str = '../models/clusterer.joblib'):
        joblib.dump(self.classifier, clf_path)
        joblib.dump(self.clusterer, clust_path)