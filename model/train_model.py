from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from config import Config


FEATURE_COLUMNS = [
    "claim_amount",
    "age_of_policy_days",
    "number_of_previous_claims",
    "location_risk_score",
    "police_report_filed",
    "witnesses",
]
TARGET_COLUMN = "is_fraud"


def _create_seed_dataset(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    seed_rows = [
        [1400, 720, 0, 0.12, 1, 2, 0],
        [21500, 35, 4, 0.88, 0, 0, 1],
        [6800, 320, 1, 0.34, 1, 1, 0],
        [42000, 21, 5, 0.95, 0, 0, 1],
        [12000, 220, 2, 0.67, 1, 0, 1],
        [2400, 900, 0, 0.10, 1, 3, 0],
        [8900, 450, 1, 0.40, 1, 1, 0],
        [31500, 47, 3, 0.91, 0, 0, 1],
        [5600, 680, 0, 0.20, 1, 2, 0],
        [27100, 65, 4, 0.86, 0, 0, 1],
        [7500, 520, 1, 0.31, 1, 1, 0],
        [19900, 110, 2, 0.75, 0, 0, 1],
        [9800, 365, 1, 0.45, 1, 1, 0],
        [41000, 18, 6, 0.98, 0, 0, 1],
        [3600, 810, 0, 0.16, 1, 2, 0],
        [24800, 90, 3, 0.82, 0, 0, 1],
        [13400, 260, 2, 0.55, 1, 0, 0],
        [29500, 55, 5, 0.93, 0, 0, 1],
        [4800, 740, 0, 0.14, 1, 2, 0],
        [17200, 180, 2, 0.62, 0, 1, 1],
    ]
    dataset = pd.DataFrame(seed_rows, columns=FEATURE_COLUMNS + [TARGET_COLUMN])
    dataset.to_csv(path, index=False)


def train_and_save_model():
    Config.MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    Config.INSURANCE_DATASET_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not Config.INSURANCE_DATASET_PATH.exists():
        _create_seed_dataset(Config.INSURANCE_DATASET_PATH)

    data = pd.read_csv(Config.INSURANCE_DATASET_PATH)
    cleaned_data = data.dropna().copy()
    cleaned_data[FEATURE_COLUMNS + [TARGET_COLUMN]].to_csv(
        Config.PROCESSED_DATASET_PATH, index=False
    )

    X = cleaned_data[FEATURE_COLUMNS]
    y = cleaned_data[TARGET_COLUMN].astype(int)

    x_train, x_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    preprocessor = ColumnTransformer(
        transformers=[("num", StandardScaler(), FEATURE_COLUMNS)]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                LogisticRegression(
                    max_iter=500,
                    class_weight="balanced",
                    random_state=42,
                ),
            ),
        ]
    )

    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    report = classification_report(y_test, predictions)

    artifact = {
        "model": model,
        "feature_columns": FEATURE_COLUMNS,
        "metadata": {
            "algorithm": "LogisticRegression",
            "version": 1,
        },
    }
    joblib.dump(artifact, Config.MODEL_PATH)
    return report


if __name__ == "__main__":
    metrics = train_and_save_model()
    print("Model trained and saved to:", Config.MODEL_PATH)
    print(metrics)
