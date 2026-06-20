import json
import os
import re
from pathlib import Path

import pickle
import numpy as np
import pandas as pd
from flask import Flask, jsonify, render_template, request

import sensor_db
BASE_DIR = Path(__file__).resolve().parent

METRICS_PATH = BASE_DIR / "metrics.json"
MODEL_PATH = BASE_DIR / "model.pkl"
META_PATH = BASE_DIR / "crop_season_meta.json"


SENSOR_API_TOKEN = os.environ.get("SENSOR_API_TOKEN", "").strip()

HOME_SENSOR_PREVIEW = 15
HISTORY_LIMIT = 100

YIELD_DISPLAY_MAX = 100.0
ACRE_TO_HECTARE = 0.404686
latest_data = {
    "temperature": 0,
    "humidity": 0,
    "soil_moisture": 0
}

def to_relative_score(value: float, reference_value: float) -> float:
    if reference_value <= 0:
        return 0.0
    score = (float(value) / float(reference_value)) * 100.0
    return max(0.0, min(score, YIELD_DISPLAY_MAX))


def parse_area_acres(text: str) -> float:
    normalized = (text or "").strip().lower()
    if not normalized:
        raise ValueError("empty area")

    match = re.search(r"[-+]?\d*\.?\d+", normalized)
    if not match:
        raise ValueError("invalid area")

    area_acres = float(match.group())
    if area_acres <= 0:
        raise ValueError("non-positive area")
    return area_acres * ACRE_TO_HECTARE


app = Flask(__name__)
sensor_db.init_db()

_model = None
_meta = None


def get_model():
    global _model
    if _model is None:
        with open(MODEL_PATH, "rb") as f:
            _model = pickle.load(f)
    return _model


def get_meta():
    global _meta
    if _meta is None:
        with open(META_PATH, encoding="utf-8") as f:
            _meta = json.load(f)
    return _meta
def get_metrics():
    if METRICS_PATH.exists():
        with open(METRICS_PATH) as f:
            return json.load(f)
    return {"r2_score": 0, "mae": 0}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    metrics = get_metrics()
    meta = get_meta()
    seasons = meta["seasons"]
    crops_by_season = meta["crops_by_season"]

    best_crop = None
    best_yield = None
    other_crops = None
    error = None
    area_val = ""
    selected_season = seasons[0] if seasons else ""

    if request.method == "POST":
        selected_season = (request.form.get("season") or "").strip()
        area_val = (request.form.get("area") or "").strip()

        if selected_season not in crops_by_season:
            error = "Invalid season selected"
        else:
            try:
                area = parse_area_acres(area_val)
            except ValueError:
                error = "Enter area like 2 acres"

        if not error:
            crops = crops_by_season[selected_season]
            model = get_model()

            latest = sensor_db.latest()

            if latest:
                soil = float(latest.get("soil_moisture", 50))
                temp = float(latest.get("temperature_c", 25))
                humidity = float(latest.get("humidity_pct", 60))
                print("SOIL FROM DB:", soil)
            else:
                soil, temp, humidity = 50, 25, 60
            

            if not crops:
                error = "No crops available"
            else:

                rows = []
                for crop in crops:
                    rows.append({
                        "Season": selected_season,
                        "Crop": crop,
                        "Area": area,
                        "Soil_Moisture": soil,
                        "Temperature": temp,
                        "Humidity": humidity
                    })

                X_pred = pd.DataFrame(rows)[[
                    "Season",
                    "Crop",
                    "Area",
                    "Soil_Moisture",
                    "Temperature",
                    "Humidity"
                ]]

                try:
                    preds = model.predict(X_pred)
                except Exception as e:
                    print("PREDICTION ERROR:", e)
                    preds = np.ones(len(X_pred))

                all_rows = []
                for season_name, season_crops in crops_by_season.items():
                    for crop_name in season_crops:
                        all_rows.append({
                            "Season": season_name,
                            "Crop": crop_name,
                            "Area": area,
                            "Soil_Moisture": soil,
                            "Temperature": temp,
                            "Humidity": humidity
                        })

                all_df = pd.DataFrame(all_rows)

                all_df = all_df[[
                    "Season",
                    "Crop",
                    "Area",
                    "Soil_Moisture",
                    "Temperature",
                    "Humidity"
                ]]

                try:
                    preds = model.predict(X_pred)
                    adjusted_preds = []

                    for i, val in enumerate(preds):
                            # normalize soil moisture (0–100)
                        soil_factor = soil / 100  

                            # adjust yield (20% influence)
                        adjusted = val * (0.8 + 0.4 * soil_factor)

                        adjusted_preds.append(adjusted)

                    preds = np.array(adjusted_preds)
                except Exception as e:
                    print("PREDICTION ERROR:", e)
                    error = "Model prediction failed"
                    preds=None

                if preds is None or len(preds) == 0:
                    error = "Prediction failed"
                    
                    
                else:
                    total_yield = float(np.sum(preds))
                    if total_yield == 0:
                        total_yield = 1
                    order = np.argsort(-preds)
                    graph_labels = [crops[int(i)] for i in order[:5]]
                    graph_values = [round(float(preds[int(i)]), 2) for i in order[:5]]
                    best_i = int(order[0])
                    best_crop = crops[best_i]
                    best_raw = float(preds[best_i])
                    best_yield = round((best_raw / total_yield) * 100, 2)

                    other_crops = [
                        (crops[int(i)], round((float(preds[int(i)]) / total_yield) * 100, 2))
                        for i in order[1:1 + min(5, len(crops) - 1)]
                    ]

    sensor_history = sensor_db.history(HOME_SENSOR_PREVIEW)

    return render_template(
        "dashboard.html",
        seasons=seasons,
        selected_season=selected_season,
        area=area_val,
        best_crop=best_crop,
        best_yield=best_yield,
        other_crops=other_crops,
        error=error,
        sensor_history=sensor_history,
        metrics=metrics,
        graph_labels=graph_labels if 'graph_labels' in locals() else [],
        graph_values=graph_values if 'graph_values' in locals() else []
    )

@app.route("/history")
def history():
    rows = sensor_db.history(100)
    return render_template("history.html", sensor_history=rows)
@app.route("/api/sensor/history")
def api_sensor_history():
    rows = sensor_db.history(100)

    return jsonify({
        "ok": True,
        "data": rows
    })
@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/api/sensor/latest")
def api_sensor_latest():
    latest = sensor_db.latest()

    if not latest:
        return jsonify({"ok": False, "data": None})

    return jsonify({
        "ok": True,
        "data": latest
    })
from flask import request, jsonify

@app.route('/api/sensor', methods=['POST'])
def receive_data():
    data = request.get_json()
    print("Received:", data)

    # ✅ SAVE TO DATABASE (IMPORTANT)
    sensor_db.add_reading(
        soil_moisture=data["soil_moisture"],
        temperature_c=data["temperature_c"],
        humidity_pct=data["humidity_pct"]
    )

    return jsonify({"ok": True}), 200



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)