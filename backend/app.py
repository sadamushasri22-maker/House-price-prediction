import sys
import os
import pandas as pd
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS

# Add project root directory to sys.path so src module resolves cleanly
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

os.chdir(project_root)

from src.pipeline.prediction_pipeline import CustomData, PredictPipeline
from src.exception import CustomException
from backend.db import find_or_create_user, save_prediction, get_user_predictions

# Determine template and static folders
dist_folder = os.path.join(project_root, "frontend", "dist")
if os.path.exists(dist_folder):
    app = Flask(
        __name__,
        static_folder=os.path.join(dist_folder, "assets"),
        template_folder=dist_folder,
    )
else:
    app = Flask(
        __name__,
        template_folder=os.path.join(project_root, "frontend", "templates"),
        static_folder=os.path.join(project_root, "frontend", "static"),
    )

CORS(app)

# Load dataset for unique city & zipcode dropdowns
try:
    df_raw = pd.read_csv(os.path.join(project_root, "data", "raw", "data.csv"))
    CITIES = sorted(df_raw["city"].unique().tolist())
    ZIPCODES = sorted(
        df_raw["statezip"]
        .apply(lambda x: str(x).split()[-1] if " " in str(x) else str(x))
        .unique()
        .tolist()
    )
except Exception:
    CITIES = ["Seattle", "Bellevue", "Redmond", "Renton", "Kirkland", "Shoreline", "Kent"]
    ZIPCODES = ["98115", "98008", "98052", "98042", "98133", "98033"]


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "app_name": "EstimaHouse AI",
        "version": "1.0.0",
        "database_connected": os.path.exists(os.path.join(project_root, "backend", "database.db")),
        "model_loaded": os.path.exists(os.path.join(project_root, "artifacts", "model_trainer", "model.pkl"))
    }), 200


@app.route("/", methods=["GET"])
def index():
    if os.path.exists(os.path.join(dist_folder, "index.html")):
        return send_from_directory(dist_folder, "index.html")
    return render_template("index.html", cities=CITIES, zipcodes=ZIPCODES, prediction=None)


@app.route("/api/auth/google", methods=["POST"])
def auth_google():
    try:
        req = request.get_json(force=True)
        email = req.get("email")
        name = req.get("name", "Google User")
        picture = req.get("picture", "")

        if not email:
            return jsonify({"status": "error", "message": "Email is required"}), 400

        user = find_or_create_user(email=email, name=name, picture=picture, provider="google")
        return jsonify({"status": "success", "user": user})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/api/auth/login", methods=["POST"])
def auth_login():
    try:
        req = request.get_json(force=True)
        email = req.get("email")
        name = req.get("name", email.split("@")[0] if email else "User")

        if not email:
            return jsonify({"status": "error", "message": "Email is required"}), 400

        user = find_or_create_user(email=email, name=name, provider="email")
        return jsonify({"status": "success", "user": user})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/api/history", methods=["GET"])
def get_history():
    try:
        email = request.args.get("email")
        if not email:
            return jsonify({"status": "error", "message": "Email query param required"}), 400

        history = get_user_predictions(user_email=email)
        return jsonify({"status": "success", "history": history})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/predict", methods=["POST"])
def predict_datapoint():
    try:
        bedrooms = int(request.form.get("bedrooms", 3))
        bathrooms = float(request.form.get("bathrooms", 2.25))
        sqft_living = int(request.form.get("sqft_living", 2000))
        sqft_lot = int(request.form.get("sqft_lot", 7500))
        floors = float(request.form.get("floors", 2.0))
        waterfront = int(request.form.get("waterfront", 0))
        view = int(request.form.get("view", 0))
        condition = int(request.form.get("condition", 3))
        sqft_above = int(request.form.get("sqft_above", 1600))
        sqft_basement = int(request.form.get("sqft_basement", 400))
        yr_built = int(request.form.get("yr_built", 1985))
        yr_renovated = int(request.form.get("yr_renovated", 0))
        city = request.form.get("city", "Seattle")
        zipcode = request.form.get("zipcode", "98115")
        user_email = request.form.get("user_email")

        data = CustomData(
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            sqft_living=sqft_living,
            sqft_lot=sqft_lot,
            floors=floors,
            waterfront=waterfront,
            view=view,
            condition=condition,
            sqft_above=sqft_above,
            sqft_basement=sqft_basement,
            yr_built=yr_built,
            yr_renovated=yr_renovated,
            city=city,
            zipcode=zipcode,
        )

        pred_df = data.get_data_as_data_frame()
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)

        if user_email:
            save_prediction(
                user_email=user_email,
                city=city,
                zipcode=zipcode,
                sqft_living=sqft_living,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                estimated_price=round(results, 2)
            )

        if os.path.exists(os.path.join(dist_folder, "index.html")):
            return send_from_directory(dist_folder, "index.html")

        return render_template(
            "index.html",
            cities=CITIES,
            zipcodes=ZIPCODES,
            prediction=results,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            sqft_living=sqft_living,
            sqft_lot=sqft_lot,
            floors=floors,
            waterfront=waterfront,
            view=view,
            condition=condition,
            sqft_above=sqft_above,
            sqft_basement=sqft_basement,
            yr_built=yr_built,
            yr_renovated=yr_renovated,
            city=city,
            zipcode=zipcode,
        )

    except Exception as e:
        raise CustomException(e, sys)


@app.route("/api/predict", methods=["POST"])
def api_predict():
    try:
        req_json = request.get_json(force=True)
        data = CustomData(
            bedrooms=int(req_json.get("bedrooms", 3)),
            bathrooms=float(req_json.get("bathrooms", 2.25)),
            sqft_living=int(req_json.get("sqft_living", 2000)),
            sqft_lot=int(req_json.get("sqft_lot", 7500)),
            floors=float(req_json.get("floors", 2.0)),
            waterfront=int(req_json.get("waterfront", 0)),
            view=int(req_json.get("view", 0)),
            condition=int(req_json.get("condition", 3)),
            sqft_above=int(req_json.get("sqft_above", 1600)),
            sqft_basement=int(req_json.get("sqft_basement", 400)),
            yr_built=int(req_json.get("yr_built", 1985)),
            yr_renovated=int(req_json.get("yr_renovated", 0)),
            city=str(req_json.get("city", "Seattle")),
            zipcode=str(req_json.get("zipcode", "98115")),
        )

        pred_df = data.get_data_as_data_frame()
        predict_pipeline = PredictPipeline()
        predicted_price = predict_pipeline.predict(pred_df)

        user_email = req_json.get("user_email")
        if user_email:
            save_prediction(
                user_email=user_email,
                city=str(req_json.get("city", "Seattle")),
                zipcode=str(req_json.get("zipcode", "98115")),
                sqft_living=int(req_json.get("sqft_living", 2000)),
                bedrooms=int(req_json.get("bedrooms", 3)),
                bathrooms=float(req_json.get("bathrooms", 2.25)),
                estimated_price=round(predicted_price, 2)
            )

        return jsonify({
            "status": "success",
            "app_name": "EstimaHouse AI",
            "estimated_price": round(predicted_price, 2),
            "currency": "USD"
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
