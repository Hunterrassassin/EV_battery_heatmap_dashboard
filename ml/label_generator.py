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

    # Add new column: risk_flag
    def determine_risk(row):
        temp_limit = get_safe_limit(row['rpm'])
        risky_temp = row['temp_c'] > temp_limit
        low_soc = row['soc_pct'] < 25
        high_current = row['current_a'] > 20
        abnormal_voltage = row['voltage_v'] < 300 or row['voltage_v'] > 410
        high_rpm = row['rpm'] > 3000

        # Compound condition for risk:
        if (
                risky_temp or
                (high_current and low_soc) or
                abnormal_voltage or
                (risky_temp and high_rpm)
        ):
            return 1
        return 0

    df['risk_flag'] = df.apply(determine_risk, axis=1)
    df.to_csv(output_csv_path, index=False)
    print(f"[✅] Smarter risk labels generated and saved to: {output_csv_path}")

if __name__ == "__main__":
    input_path = "data/synthetic_battery_data.csv"
    output_path = "data/battery_labeled.csv"
    label_risk(input_path, output_path)
