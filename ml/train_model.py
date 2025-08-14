import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

# Load preprocessed feature and label arrays
X = np.load("data/X.npy")
y = np.load("data/y.npy")

unique, counts = np.unique(y, return_counts=True)
print(dict(zip(unique, counts)))


# Split into train/test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

#Evaluate
y_pred = model.predict(X_test)
print("[📊] Classification Report:")
print(classification_report(y_test, y_pred))
print(f"[✅] Accuracy: {accuracy_score(y_test, y_pred):.2f}")

# Save the trained model
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/risk_predictor.pkl")
print("[💾] Model saved to models/risk_predictor.pkl")
