import os
import numpy as np
import joblib
from flask import Flask, render_template,request
from analysis.parser import load_log_data


app = Flask(__name__)

model = joblib.load("models/risk_predictor.pkl")
scaler = joblib.load("models/scaler.pkl")

@app.route("/")
def dashboard():

    # Load battery data
    data = load_log_data()
    alerts = []

    if data is not None and 'risk_flag' in data.columns:
        risky_rows = data[data['risk_flag'] == 1]
        for _, row in risky_rows.iterrows():
            alerts.append(
                f"Row {_}: Temp = {row['temp_c']}°C,SOC = {row['soc_pct']}%, RPM = {row['rpm']}"
            )

    # Load heatmaps from static/heatmaps/
    image_folder = os.path.join('static', 'heatmaps')


    image_files = [
        f"heatmaps/{f}"
        for f in os.listdir(image_folder)
        if f.lower().endswith('.png')
    ]
    print("[DEBUG] Image files found:", image_files)
  #  print("[DEBUG] Alerts generated:", alerts)
    return render_template("dashboard.html", alerts=alerts, images=image_files)




@app.route("/predict",methods=["POST"])
def predict():
    try:
        temp_c = float(request.form["temp_c"])
        voltage_v = float(request.form["voltage_v"])
        current_a = float(request.form["current_a"])
        soc_pct = float(request.form["soc_pct"])
        rpm = float(request.form["rpm"])

        # Get input prediction
        features = np.array([[temp_c, voltage_v, current_a, soc_pct, rpm]])
        scaler = joblib.load("models/scaler.pkl")
        model = joblib.load("models/risk_predictor.pkl")
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)[0]

        # Get heatmap images
        image_folder = os.path.join('static', 'heatmaps')
        image_files = [f"heatmaps/{f}" for f in os.listdir(image_folder) if f.lower().endswith('.png')]

        # ⚠️ Generate alerts from dataset
        data = load_log_data()
        alerts = []
        if data is not None and 'risk_flag' in data.columns:
            risky_rows = data[data['risk_flag'] == 1]
            for _, row in risky_rows.iterrows():
                alerts.append(
                    f"⚠️ Risk = 1 at {row['timestamp']}s | Temp = {row['temp_c']}°C, SOC = {row['soc_pct']}%, RPM = {row['rpm']}"
                )

        # Set prediction result
        prediction_result = "🚨 Risky" if prediction == 1 else "✅ Safe"

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