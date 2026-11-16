from flask import Blueprint, flash, redirect, render_template, request, url_for
from services.prediction_service import PredictionService, PredictionInputError
from models.database import save_prediction, get_recent_predictions

prediction_bp = Blueprint("prediction", __name__)

@prediction_bp.post("/predict")
def predict():
    try:
        form_data = {
            "age": request.form.get("age", ""),
            "annual_income": request.form.get("annual_income", ""),
            "website_visits": request.form.get("website_visits", ""),
            "previous_purchases": request.form.get("previous_purchases", ""),
            "time_on_website": request.form.get("time_on_website", ""),
            "discount_offered": request.form.get("discount_offered", ""),
        }
        result = PredictionService.predict(form_data)
        save_prediction(form_data, result)
        return render_template("result.html", result=result, inputs=form_data)
    except (PredictionInputError, FileNotFoundError, RuntimeError) as exc:
        flash(str(exc), "error")
        return redirect(url_for("home"))

@prediction_bp.get("/history")
def history():
    records = get_recent_predictions(limit=100)
    return render_template("history.html", records=records)
