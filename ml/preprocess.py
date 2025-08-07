import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import os

def preprocess(csv_path):
    df = pd.read_csv(csv_path)

    features = ['temp_c', 'voltage_v', 'current_a', 'soc_pct','rpm']
    target = 'risk_level'

    X = df[features].values
    y = df[target].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    os.makedirs("data", exist_ok=True)
    os.makedirs("models", exist_ok=True)

    # Save preprocessed data
    np.save("data/X.npy", X_scaled)
    np.save("data/y.npy", y)

    #Save scaled data
    joblib.dump(scaler, "models/scaler.pkl")

    print("Preprocessing complete. Saved as X.npy and y.npy")

if __name__ == "__main__":
    preprocess("data/battery_labeled.csv")
