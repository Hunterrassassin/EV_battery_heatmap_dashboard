import os
import pandas as pd
import numpy as np
import joblib
from flask import Flask, render_template, request, jsonify
from analysis.parser import load_log_data
from datetime import datetime, timedelta
from gmail_service import send_email



app = Flask(__name__)

# Load models (once)
time_to_failure_model = joblib.load(os.path.join(os.path.dirname(__file__), "models", "time_to_failure_model.pkl"))
model = joblib.load(os.path.join(os.path.dirname(__file__), "models", "risk_predictor.pkl"))
scaler = joblib.load(os.path.join(os.path.dirname(__file__), "models", "scaler.pkl"))

severity_map = {0: "✅ Safe", 1: "⚠️ Moderate", 2: "🚨 High"}

@app.route("/")
def dashboard():
    data = load_log_data()
    alerts = []
    if data is not None and 'risk_level' in data.columns:
        risky_rows = data[data['risk_level'] > 0]
        for idx, row in risky_rows.iterrows():
            severity = severity_map.get(int(row['risk_level']), "Unknown")
            alerts.append(
                f"{severity} | Row {idx} | Temp = {row['temp_c']}°C, SOC = {row['soc_pct']}%, RPM = {row['rpm']}"
            )

    image_folder = os.path.join('static', 'heatmaps')
    image_files = [f"heatmaps/{f}" for f in os.listdir(image_folder) if f.lower().endswith('.png')]

    return render_template("dashboard.html", alerts=alerts, images=image_files)


@app.route('/time_to_failure_data')
def time_to_failure_data():


    try:
        df = pd.read_csv('data/battery_labeled_with_time.csv')

        # Prepare features
        X = df[['temp_c', 'voltage_v', 'current_a', 'soc_pct', 'rpm']]

        # Predict time to failure
        preds = time_to_failure_model.predict(X)
        df['predicted_time_to_failure'] = preds.astype(float)

        # Risk classification (High Risk = failure in < 10 minutes)
        df['risk_level'] = df['predicted_time_to_failure'].apply(
            lambda x: "High Risk" if x < 3600 else "Low/Medium"
        )

        # Keep only High Risk rows
        df = df[df['risk_level'] == "High Risk"]

        # Sort by shortest predicted time to failure and take top 10
        df = df.sort_values(by='predicted_time_to_failure', ascending=True).head(10)

        # ✅ Send email if any critical case is detected (< 5 minutes)
        for _, row in df.iterrows():
            if row['predicted_time_to_failure'] <= 3600:  # 5 minutes
                battery_id = row.get('Battery_ID', 'Unknown')
                send_email(
                    "raunit1819@gmail.com",
                    f"⚠️ Battery {battery_id} Critical Alert!",
                    f"Battery {battery_id} is predicted to fail in {int(row['predicted_time_to_failure'])} seconds.\n"
                    f"Please take immediate action!"
                )

        # Convert to display-friendly time left (mm:ss format)
        df['time_left'] = pd.to_timedelta(df['predicted_time_to_failure'], unit='s').astype(str)

        # Build timestamp for frontend (string)
        if 'time_seconds' in df.columns:
            # create readable HH:MM:SS relative timestamps based on now
            base = datetime.now()
            df['timestamp'] = [
                (base + timedelta(seconds=int(s))).strftime("%H:%M:%S")
                for s in df['time_seconds']
            ]
        else:
            # fallback: just give row index as timestamp-like string
            df['timestamp'] = df.index.astype(str)

        return jsonify(df.to_dict(orient='records'))

    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/predict", methods=["POST"])
def predict():
    try:
        temp_c = float(request.form["temp_c"])
        voltage_v = float(request.form["voltage_v"])
        current_a = float(request.form["current_a"])
        soc_pct = float(request.form["soc_pct"])
        rpm = float(request.form["rpm"])

        # Prepare & scale features for risk classifier
        features = np.array([[temp_c, voltage_v, current_a, soc_pct, rpm]])
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)[0]

        # Load heatmaps
        image_folder = os.path.join('static', 'heatmaps')
        image_files = [f"heatmaps/{f}" for f in os.listdir(image_folder) if f.lower().endswith('.png')]

        # Generate alerts
        data = load_log_data()
        alerts = []
        if data is not None and 'risk_level' in data.columns:
            risky_rows = data[data['risk_level'] > 0]
            for idx, row in risky_rows.iterrows():
                severity = severity_map.get(int(row['risk_level']), "Unknown")
                alerts.append(
                    f"{severity} | Row {idx} | Temp = {row['temp_c']}°C, SOC = {row['soc_pct']}%, RPM = {row['rpm']}"
                )

        prediction_result = severity_map.get(int(prediction), "Unknown")

        return render_template(
            "dashboard.html",
            alerts=alerts,
            images=image_files,
            prediction_result=prediction_result
        )

    except Exception as e:
        return f"Error occurred: {e}"


if __name__ == "__main__":
    app.run(debug=True)