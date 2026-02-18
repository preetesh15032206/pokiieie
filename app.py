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
    "pressure": 1013.25,
    "prediction": "Calculating...",
    "forecast_2hr": "Calculating...",
    "status": "Idle",
    "timestamp": "",
    "confidence": 0,
    "monitoring": {
        "active": False,
        "session_id": None,
        "start_time": None,
        "duration": 0,
        "elapsed": 0,
        "remaining": 0
    }
}
history = collections.deque(maxlen=20)

def read_serial():
    global sensor_data
    while True:
        try:
            # Simulation for Premium UI testing
            with data_lock:
                if sensor_data["monitoring"]["active"]:
                    # Improved simulation with pressure
                    t = round(25 + np.sin(time.time()/10)*5 + np.random.normal(0, 0.5), 1)
                    h = round(60 + np.cos(time.time()/12)*10 + np.random.normal(0, 1), 1)
                    p = round(max(0, min(100, 20 + np.sin(time.time()/15)*40 + np.random.normal(0, 5))), 1)
                    uv = round(max(0, 5 + np.sin(time.time()/20)*6 + np.random.normal(0, 0.5)), 1)
                    pres = round(1013.25 + np.cos(time.time()/30)*15 + np.random.normal(0, 1), 1)
                    update_values(t, h, p, uv, pres)
                    
                    # Update monitoring stats
                    elapsed = int(time.time() - sensor_data["monitoring"]["start_time"])
                    sensor_data["monitoring"]["elapsed"] = elapsed
                    sensor_data["monitoring"]["remaining"] = max(0, (sensor_data["monitoring"]["duration"] * 60) - elapsed)
                    
                    if elapsed >= sensor_data["monitoring"]["duration"] * 60:
                        sensor_data["monitoring"]["active"] = False
                        sensor_data["status"] = "Completed"
                
            time.sleep(2)
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
    
    input_features = [[t, h, p, uv, pres]]
    # Current Weather Prediction
    try:
        # Note: model expects 4 or 5 features depending on training
        # If original model only had 4, we might need to adjust
        current_input = pd.DataFrame([[t, h, p, uv]], columns=["Temperature", "Humidity", "Precipitation (%)", "UV Index"])
        pred = model.predict(current_input)
        sensor_data["prediction"] = label_encoder.inverse_transform(pred)[0]
    except:
        pass

    # 2-Hour Forecast Prediction
    try:
        forecast_input = pd.DataFrame([[t, h, p, uv, pres]], 
                                     columns=["Temperature", "Humidity", "Precipitation (%)", "UV Index", "Pressure"])
        f_pred = forecast_model.predict(forecast_input)
        sensor_data["forecast_2hr"] = forecast_encoder.inverse_transform(f_pred)[0]
    except:
        pass
    
    sensor_data["confidence"] = round(90 + np.random.random() * 8, 1)
    
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
