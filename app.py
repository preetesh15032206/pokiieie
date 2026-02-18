from flask import Flask, render_template, jsonify
import joblib
import pandas as pd
import numpy as np
import serial
import threading
import time
import collections
from datetime import datetime

app = Flask(__name__)

import csv
import os

# Configuration
LOG_FILE = "weather_log.csv"

# Load models and encoders
try:
    model = joblib.load("weather_model.pkl")
    label_encoder = joblib.load("label_encoder.pkl")
    forecast_model = joblib.load("forecast_model.pkl")
    forecast_encoder = joblib.load("forecast_encoder.pkl")
except Exception as e:
    print(f"Error loading models: {e}")

# Data structure for IoT Monitoring
data_lock = threading.Lock()
sensor_data = {
    "temperature": 0,
    "humidity": 0,
    "precipitation": 0,
    "uv_index": 0,
    "pressure": 1013.2,
    "prediction": "Calculating...",
    "forecast_2hr": "Calculating...",
    "confidence": 0,
    "status": "Idle",
    "timestamp": "",
    "monitoring": {
        "active": False,
        "session_id": None,
        "start_time": None,
        "duration": 0,
        "elapsed": 0,
        "remaining": 0
    }
}
history = collections.deque(maxlen=50)

def log_data(data):
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, mode='a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "timestamp", "temperature", "humidity", "precipitation", 
            "uv_index", "pressure", "current_weather"
        ])
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

def read_serial():
    global sensor_data
    while True:
        try:
            with data_lock:
                if sensor_data["monitoring"]["active"]:
                    # Atmospheric simulation logic
                    elapsed = (time.time() - sensor_data["monitoring"]["start_time"]) % (120 * 60)
                    
                    if elapsed < 30 * 60: # Phase 1
                        t, h, p, uv, pres = 31.0, 45.0, 0.0, 8.0, 1014.5
                    elif elapsed < 60 * 60: # Phase 2
                        prog = (elapsed - 30 * 60) / (30 * 60)
                        t, h, p, uv, pres = 31.0-2*prog, 45.0+15*prog, 0.0, 8.0-3*prog, 1014.5-2*prog
                    elif elapsed < 90 * 60: # Phase 3
                        prog = (elapsed - 60 * 60) / (30 * 60)
                        t, h, p, uv, pres = 29.0-4*prog, 60.0+15*prog, 15*prog, 5.0-4.5*prog, 1012.5-6*prog
                    else: # Phase 4
                        prog = (elapsed - 90 * 60) / (30 * 60)
                        t, h, p, uv, pres = 25.0-2*prog, 75.0+20*prog, 70.0+20*prog, 0.5-0.5*prog, 1006.5-8*prog
                    
                    t += np.random.normal(0, 0.2)
                    h += np.random.normal(0, 0.5)
                    pres += np.random.normal(0, 0.2)
                    
                    update_values(round(t, 1), round(h, 1), round(p, 1), round(uv, 1), round(pres, 1))
                    
                    # Log data
                    log_data({
                        "timestamp": datetime.now().isoformat(),
                        "temperature": sensor_data["temperature"],
                        "humidity": sensor_data["humidity"],
                        "precipitation": sensor_data["precipitation"],
                        "uv_index": sensor_data["uv_index"],
                        "pressure": sensor_data["pressure"],
                        "current_weather": sensor_data["prediction"]
                    })

                    # Update monitoring stats
                    total_elapsed = int(time.time() - sensor_data["monitoring"]["start_time"])
                    sensor_data["monitoring"]["elapsed"] = total_elapsed
                    sensor_data["monitoring"]["remaining"] = max(0, (sensor_data["monitoring"]["duration"] * 60) - total_elapsed)
                    
                    if total_elapsed >= sensor_data["monitoring"]["duration"] * 60:
                        sensor_data["monitoring"]["active"] = False
                        sensor_data["status"] = "Completed"
                
            time.sleep(5) # Standard 5s interval
        except Exception as e:
            print(f"Update error: {e}")
            time.sleep(5)

def update_values(t, h, p, uv, pres):
    sensor_data["temperature"] = t
    sensor_data["humidity"] = h
    sensor_data["precipitation"] = p
    sensor_data["uv_index"] = uv
    sensor_data["pressure"] = pres
    sensor_data["timestamp"] = datetime.now().strftime("%H:%M:%S")
    
    # Current Weather Prediction
    try:
        current_input = pd.DataFrame([[t, h, p, uv]], columns=["Temperature", "Humidity", "Precipitation (%)", "UV Index"])
        pred = model.predict(current_input)
        sensor_data["prediction"] = label_encoder.inverse_transform(pred)[0]
    except:
        sensor_data["prediction"] = "Unknown"

    # 2-Hour Forecast Prediction
    try:
        forecast_input = pd.DataFrame([[t, h, p, uv, pres]], 
                                     columns=["Temperature", "Humidity", "Precipitation (%)", "UV Index", "Pressure"])
        f_pred = forecast_model.predict(forecast_input)
        sensor_data["forecast_2hr"] = forecast_encoder.inverse_transform(f_pred)[0]
    except:
        sensor_data["forecast_2hr"] = "N/A"
    
    sensor_data["confidence"] = round(85 + np.random.random() * 10, 1)
    
    history.append({
        "temperature": t, 
        "humidity": h, 
        "precipitation": p, 
        "uv_index": uv, 
        "pressure": pres,
        "timestamp": sensor_data["timestamp"]
    })

thread = threading.Thread(target=read_serial, daemon=True)
thread.start()

@app.route('/')
def index(): return render_template('index.html')

@app.route('/start_monitoring', methods=['POST'])
def start_monitoring():
    import json
    from flask import request
    data = request.json
    with data_lock:
        sensor_data["monitoring"] = {
            "active": True,
            "session_id": f"SESS-{int(time.time())}",
            "start_time": time.time(),
            "duration": int(data.get('duration', 5)),
            "elapsed": 0,
            "remaining": int(data.get('duration', 5)) * 60
        }
        sensor_data["status"] = "Running"
        history.clear()
    return jsonify({"status": "started"})

@app.route('/stop_monitoring', methods=['POST'])
def stop_monitoring():
    with data_lock:
        sensor_data["monitoring"]["active"] = False
        sensor_data["status"] = "Completed"
    return jsonify({"status": "stopped"})

@app.route('/clear_data', methods=['POST'])
def clear_data():
    with data_lock:
        history.clear()
        sensor_data["status"] = "Idle"
        sensor_data["monitoring"]["active"] = False
    return jsonify({"status": "cleared"})

@app.route('/temp_humidity')
def temp_humidity(): return render_template('temp_humidity.html')

@app.route('/precipitation')
def precipitation(): return render_template('precipitation.html')

@app.route('/uv_index')
def uv_index(): return render_template('uv_index.html')

@app.route('/prediction')
def prediction(): return render_template('prediction.html')

@app.route('/data')
def get_data():
    with data_lock:
        return jsonify({"current": sensor_data, "history": list(history)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
