from pathlib import Path
import joblib
import pandas as pd
from config import Config

class PredictionInputError(ValueError):
    """Raised when submitted customer data is invalid."""

class PredictionService:
    @staticmethod
    def _load_model():
        model_path = Path(Config.MODEL_PATH)
        features_path = Path(Config.FEATURE_COLUMNS_PATH)
        if not model_path.exists() or not features_path.exists():
            raise FileNotFoundError(
                "Trained model not found. Run: python ml/train_model.py"
            )
        return joblib.load(model_path), joblib.load(features_path)

    @staticmethod
    def predict(form_data):
        limits = {
            "age": (18, 100, "Age"),
            "annual_income": (0, 100_000_000, "Annual income"),
            "website_visits": (0, 100_000, "Website visits"),
            "previous_purchases": (0, 100_000, "Previous purchases"),
            "time_on_website": (0, 100_000, "Time on website"),
            "discount_offered": (0, 100, "Discount offered"),
        }

        values = {}
        for key, (minimum, maximum, label) in limits.items():
            raw = str(form_data.get(key, "")).strip()
            try:
                value = float(raw)
            except (TypeError, ValueError):
                raise PredictionInputError(f"{label} must be a valid number.")
            if not value.is_integer():
                raise PredictionInputError(f"{label} must be a whole number.")
            value = int(value)
            if not minimum <= value <= maximum:
                raise PredictionInputError(
                    f"{label} must be between {minimum} and {maximum}."
                )
            values[key] = value

        model, feature_columns = PredictionService._load_model()
        row = pd.DataFrame([{
            "Age": values["age"],
            "Annual_Income": values["annual_income"],
            "Website_Visits": values["website_visits"],
            "Previous_Purchases": values["previous_purchases"],
            "Time_On_Website": values["time_on_website"],
            "Discount_Offered": values["discount_offered"],
        }], columns=feature_columns)

        prediction = int(model.predict(row)[0])
        probabilities = model.predict_proba(row)[0]
        classes = list(model.classes_)
        purchase_probability = float(probabilities[classes.index(1)]) * 100

        return {
            "prediction": prediction,
            "label": "Likely to purchase" if prediction == 1 else "Unlikely to purchase",
            "probability": round(purchase_probability, 2),
        }
