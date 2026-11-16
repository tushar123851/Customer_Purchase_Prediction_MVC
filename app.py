
from flask import Flask, render_template

from config import Config
from models.database import init_db
from controllers.prediction_controller import prediction_bp


# ==========================================
# CREATE FLASK APPLICATION
# ==========================================

def create_app():

    # Create Flask application
    app = Flask(__name__)

    # Load project configuration
    app.config.from_object(Config)

    # ======================================
    # REGISTER BLUEPRINTS (CONTROLLERS)
    # ======================================

    app.register_blueprint(prediction_bp)

    # ======================================
    # INITIALIZE SQLITE DATABASE
    # ======================================

    with app.app_context():

        init_db()

        print("Database initialized successfully!")

    # ======================================
    # HOME PAGE ROUTE
    # ======================================

    @app.route("/")
    def home():

        return render_template("index.html")

    # Return application
    return app


# ==========================================
# INITIALIZE APPLICATION
# ==========================================

app = create_app()


# ==========================================
# RUN FLASK DEVELOPMENT SERVER
# ==========================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
