from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "model"
DATABASE_DIR = BASE_DIR / "database"
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "claimwatch-dev-secret-key")
    DATABASE_PATH = DATABASE_DIR / "db.sqlite3"
    MODEL_PATH = MODEL_DIR / "fraud_model.pkl"
    INSURANCE_DATASET_PATH = DATA_DIR / "insurance_claims.csv"
    PROCESSED_DATASET_PATH = DATA_DIR / "processed_data.csv"
    
    # Email Configuration
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", True)
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "noreply@claimwatch.ai")
