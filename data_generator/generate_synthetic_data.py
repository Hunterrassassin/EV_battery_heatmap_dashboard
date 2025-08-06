import pandas as pd
import numpy as np

np.random.seed(42)
num_samples = 300

temp_c = np.random.normal(50, 10, num_samples)
voltage_v = np.random.normal(360, 10, num_samples)
current_a = np.random.normal(20, 5, num_samples)
soc_pct = np.random.uniform(20, 100, num_samples)
rpm = np.random.normal(3000, 500, num_samples)



risk_flag = ((temp_c > 50) | (voltage_v > 380) | (current_a > 30)).astype(int)

df = pd.DataFrame({
    "temp_c": temp_c,
    "voltage_v": voltage_v,
    "current_a": current_a,
    "soc_pct": soc_pct,
    "rpm": rpm,
    "risk_flag": risk_flag
})

df.to_csv("data/synthetic_battery_data.csv", index=False)
print("✅ Synthetic dataset saved as 'synthetic_battery_data.csv'")
