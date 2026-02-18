from pathlib import Path

import joblib
import pandas as pd

from config import Config
from model.train_model import train_and_save_model


def ensure_model_exists():
    model_path = Path(Config.MODEL_PATH)
    if not model_path.exists():
        train_and_save_model()
        return

    try:
        artifact = joblib.load(model_path)
        if "model" not in artifact or "feature_columns" not in artifact:
            raise ValueError("Invalid model artifact format.")
    except Exception:
        train_and_save_model()


def predict_claim(feature_dict: dict):
    ensure_model_exists()
    artifact = joblib.load(Config.MODEL_PATH)
    model = artifact["model"]
    feature_columns = artifact["feature_columns"]

    missing_columns = [column for column in feature_columns if column not in feature_dict]
    if missing_columns:
        raise ValueError(f"Missing required input fields: {', '.join(missing_columns)}")

    input_frame = pd.DataFrame([{column: feature_dict[column] for column in feature_columns}])
    probabilities = model.predict_proba(input_frame)[0]
    fraud_probability = float(probabilities[1])
    label = "Fraud" if fraud_probability >= 0.5 else "Legitimate"
    return label, fraud_probability
