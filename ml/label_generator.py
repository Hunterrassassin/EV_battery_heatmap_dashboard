import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from analysis.thresholds import get_safe_limit

def label_risk(input_csv_path, output_csv_path):
    if not os.path.exists(input_csv_path):
        print(f"[ERROR] File not found: {input_csv_path}")
        return

    df = pd.read_csv(input_csv_path)

    # Add new column: risk_level
    def determine_severity(row):
        score = 0

        # Temperature & RPM interaction
        if row['temp_c'] > 65 and row['rpm'] > 3500:
            score += 3
        elif row['temp_c'] > 60:
            score += 2
        elif row['temp_c'] > 50:
            score += 1

        # SOC & Current relationship
        if row['soc_pct'] < 20 and row['current_a'] > 25:
            score += 2
        elif row['soc_pct'] < 30:
            score += 1

        # Current alone
        if row['current_a'] > 26:
            score += 2
        elif row['current_a'] > 22:
            score += 1

        # Voltage sanity check
        if row['voltage_v'] < 320 or row['voltage_v'] > 420:
            score += 1

        # RPM alone
        if row['rpm'] > 4000:
            score += 2
        elif row['rpm'] > 3000:
            score += 1

        # Final severity classification
        if score >= 4:
            return 2  # High Risk
        elif score >= 3:
            return 1  # Moderate Risk
        else:
            return 0  # Safe

    df['risk_level'] = df.apply(determine_severity, axis=1)
    df.to_csv(output_csv_path, index=False)
    print(f" risk levels generated and saved to: {output_csv_path}")

if __name__ == "__main__":
    input_path = "data/synthetic_battery_data.csv"
    output_path = "data/battery_labeled.csv"
    label_risk(input_path, output_path)
