import serial
import joblib
import pandas as pd
import time

# -----------------------------
# LOAD TRAINED MODEL
# -----------------------------
model = joblib.load("weather_model.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# -----------------------------
# CONNECT TO ARDUINO
# ⚠ Change COM7 if needed
# -----------------------------
ser = serial.Serial("COM7", 9600, timeout=1)

print("Listening to Arduino...\n")
time.sleep(2)  # wait for serial to stabilize

while True:
    try:
        line = ser.readline().decode('utf-8').strip()

        if line:
            print("Raw Data:", line)

            values = line.split(",")

            if len(values) == 4:
                temperature = float(values[0])
                humidity = float(values[1])
                precipitation = float(values[2])
                uv_index = float(values[3])

                # Create DataFrame with SAME columns used in training
                input_data = pd.DataFrame(
                    [[temperature, humidity, precipitation, uv_index]],
                    columns=["Temperature", "Humidity", "Precipitation (%)", "UV Index"]
                )

                # Predict
                prediction = model.predict(input_data)
                weather_type = label_encoder.inverse_transform(prediction)

                print("Predicted Weather:", weather_type[0])
                print("----------------------------------")

    except Exception as e:
        print("Error:", e)
