import pandas as pd
import os

# Paths
DATA_DIR = os.path.join("data")
INPUT_FILE = os.path.join(DATA_DIR, "battery_labeled.csv")
OUTPUT_FILE = os.path.join(DATA_DIR, "battery_labeled_with_time.csv")

# Read original CSV
df = pd.read_csv(INPUT_FILE)

# Add time in seconds (0, 5, 10, 15, ...)
df["time_seconds"] = [i * 5 for i in range(len(df))]

# Save new CSV
df.to_csv(OUTPUT_FILE, index=False)

print(f"✅ time_seconds column added. File saved at: {OUTPUT_FILE}")
