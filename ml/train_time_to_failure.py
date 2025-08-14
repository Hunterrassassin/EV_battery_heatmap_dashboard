# File: ml/train_time_to_failure.py

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# =====================
# 1. Load the dataset
# =====================
data_path = "data/battery_labeled_with_time.csv"  # Path to the CSV generated in Step 1
df = pd.read_csv(data_path)

# =====================================
# 2. Create the "time_to_failure" target
# =====================================
# For demo purposes, we simulate "time to failure" based on temperature & SOC trends
# The idea: higher temp & lower SOC → quicker failure
max_time = 5000  # seconds (you can adjust this)
df["time_to_failure"] = max_time - (df["temp_c"] * 15 + (100 - df["soc_pct"]) * 10)

# Ensure no negative times
df["time_to_failure"] = df["time_to_failure"].clip(lower=0)

# ==============================
# 3. Select features and target
# ==============================
features = ["temp_c", "voltage_v", "current_a", "soc_pct", "rpm"]  # Adjust based on your CSV columns
X = df[features]
y = df["time_to_failure"]

# ===============================
# 4. Train-test split
# ===============================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ===============================
# 5. Train regression model
# ===============================
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ===============================
# 6. Evaluate the model
# ===============================
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Model Performance:")
print(f"  MSE: {mse:.2f}")
print(f"  R² Score: {r2:.2f}")

# ===============================
# 7. Save the model
# ===============================
model_path = "models/time_to_failure_model.pkl"
joblib.dump(model, model_path)
print(f"✅ Model saved to {model_path}")
