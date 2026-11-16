import sqlite3
from pathlib import Path
from flask import current_app

def _connect():
    db_path = Path(current_app.config["DATABASE_PATH"])
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    with _connect() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                age INTEGER NOT NULL,
                annual_income INTEGER NOT NULL,
                website_visits INTEGER NOT NULL,
                previous_purchases INTEGER NOT NULL,
                time_on_website INTEGER NOT NULL,
                discount_offered INTEGER NOT NULL,
                prediction INTEGER NOT NULL,
                probability REAL NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

def save_prediction(inputs, result):
    with _connect() as connection:
        connection.execute("""
            INSERT INTO predictions (
                age, annual_income, website_visits, previous_purchases,
                time_on_website, discount_offered, prediction, probability
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            int(inputs["age"]),
            int(inputs["annual_income"]),
            int(inputs["website_visits"]),
            int(inputs["previous_purchases"]),
            int(inputs["time_on_website"]),
            int(inputs["discount_offered"]),
            result["prediction"],
            result["probability"],
        ))

def get_recent_predictions(limit=100):
    with _connect() as connection:
        rows = connection.execute(
            "SELECT * FROM predictions ORDER BY id DESC LIMIT ?",
            (limit,)
        ).fetchall()
    return [dict(row) for row in rows]
