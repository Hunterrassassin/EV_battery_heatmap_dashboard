# 🔋 EV Battery Heatmap Dashboard

A dynamic data visualization tool for detecting thermal stress in EV batteries using real-time CSV telemetry logs. Built using Python, Flask, and Matplotlib — designed to assist FSAE teams and EV engineers in making critical thermal decisions.

---

## 🚀 Features

- 📈 Generates heatmaps from time-series battery logs (temperature, RPM, SOC, etc.)
- ⚠️ Highlights dangerous temperature zones exceeding safe limits
- 📊 Displays multiple heatmaps dynamically on a professional web dashboard
- 💡 Rule-based alert system using RPM-based temperature thresholds
- 💻 Clean UI with live annotations and thermal zone summaries

---

## 🛠️ Tech Stack

- **Python**
- **Flask**
- **Matplotlib / Seaborn**
- **Pandas**
- **HTML + CSS (Orbitron Theme)**

---

## 📁 Folder Structure

ev_battery_heatmap/
│
├── - app/ # Flask app backend
│ ├── app.py # Main app file
│ ├── static/ # Heatmap images are stored here
│ │ └── heatmaps/
│ └── templates/
│ └── dashboard.html # Frontend dashboard
│
├── analysis/ # Data processing logic
│ ├── parser.py
│ └── thresholds.py
│
├── data/
│ └── battery_log_sample.csv
│ └── battery_log_large.csv
│
├── tests/
│ └── test_parser.py
│
├── requirements.txt
├── README.md
└── .gitignore



---

##🧪 Sample Log Format

```csv
timestamp,temp_c,voltage_v,current_a,soc_pct,rpm
0,32.5,360.1,14.5,98.0,1000
1,33.0,359.8,14.2,97.8,1200
2,34.8,359.4,13.9,97.6,1400
.....,....,.....,...,..,.,.
```
## ⚙️ How to Run Locally
1. Clone the Repository

- git clone  https://github.com/Hunterrassassin/ev_battery_heatmap_dashboard.git
- cd ev-battery-heatmap-dashboard
2. Create Virtual Environment
- python -m venv .venv
- For Windows
  - .venv\Scripts\activate
- For macOS/Linux
  - source .venv/bin/activate
3. Install Dependencies
- pip install -r requirements.txt
4. Run the App
- python app/app.py
- Visit the dashboard at:
👉 http://127.0.0.1:5000/
---

## 🧪 Example Output
✅ All zones are within safe temperature limits
OR
🚨 Alerts like:
⚠️ Temp = 45.2°C at 8s | RPM = 3000 (limit: 40.0°C)

---

## 👨‍💻 Developed by
- **Sanidhiya Gupta**


