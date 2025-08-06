import joblib
import numpy as np

# Load the trained model
model = joblib.load("models/risk_predictor.pkl")
scaler = joblib.load("models/scaler.pkl")

# Define sample input
sample_input = np.array([[45, 360, 8, 65, 3500]])  # temp, voltage, current, soc, rpm

#Scale the input
scaled_input = scaler.transform(sample_input)

# Predict
prediction = model.predict(sample_input)[0]
print("Predicted Label:", prediction)
