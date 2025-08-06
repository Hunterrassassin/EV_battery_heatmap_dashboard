import pandas as pd
import os


def load_log_data():
    file_path = os.path.join("data", "battery_labeled.csv")

    if not os.path.exists(file_path):
        print("❌ Log file not found:", file_path)
        return None

    try:
        df = pd.read_csv(file_path)
        print("✅ Log file loaded successfully.")
     #  print(df.head())  # Show first 5 rows for sanity check
        return df
    except Exception as e:
        print("❌ Error reading CSV:", e)
        return None


# Run this only if called directly
if __name__ == "__main__":
    load_log_data()
