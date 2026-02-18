import sqlite3
from pathlib import Path

from config import Config
from utils.helpers import hash_password


def init_db(db_path: Path | None = None):
    final_db_path = db_path or Config.DATABASE_PATH
    final_db_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(final_db_path)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'analyst',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS claims (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            claimant_name TEXT NOT NULL,
            claimant_email TEXT NOT NULL,
            claimant_age INTEGER,
            claimant_gender TEXT,
            claim_amount REAL NOT NULL,
            claim_type TEXT NOT NULL,
            incident_date TEXT NOT NULL,
            description TEXT,
            claim_image TEXT,
            age_of_policy_days INTEGER NOT NULL,
            number_of_previous_claims INTEGER NOT NULL,
            location_risk_score REAL NOT NULL,
            police_report_filed INTEGER NOT NULL,
            police_report_number TEXT,
            witnesses INTEGER NOT NULL,
            prediction_label TEXT NOT NULL,
            prediction_score REAL NOT NULL,
            email_sent INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """
    )

    admin = cursor.execute(
        "SELECT id FROM users WHERE username = ?", ("admin",)
    ).fetchone()
    if not admin:
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            ("admin", hash_password("admin123"), "admin"),
        )

    analyst = cursor.execute(
        "SELECT id FROM users WHERE username = ?", ("analyst",)
    ).fetchone()
    if not analyst:
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            ("analyst", hash_password("analyst123"), "analyst"),
        )

    connection.commit()
    connection.close()


if __name__ == "__main__":
    init_db()
    print(f"Database initialized at: {Config.DATABASE_PATH}")
