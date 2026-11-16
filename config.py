import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-development-secret")
    DATABASE_PATH = os.path.join(BASE_DIR, "instance", "predictions.db")
    MODEL_PATH = os.path.join(BASE_DIR, "ml", "saved_model", "purchase_model.joblib")
    FEATURE_COLUMNS_PATH = os.path.join(BASE_DIR, "ml", "saved_model", "feature_columns.joblib")
