import joblib
import pandas as pd

# -----------------------------
# Load trained model & encoder
# -----------------------------
model = joblib.load("weather_model.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# -----------------------------
# Example Sensor Values
# (Try different combinations)
# -----------------------------

temperature = 38        # °C (High temp)
humidity = 30           # % (Low humidity)
precipitation = 0       # % (No rain)
uv_index = 10           # UV scale (High sunlight)

# -----------------------------
# Create DataFrame with SAME
# column names used in training
# -----------------------------

input_data = pd.DataFrame(
    [[temperature, humidity, precipitation, uv_index]],
    columns=[
        "Temperature",
        "Humidity",
        "Precipitation (%)",
        "UV Index"
    ]
)

# -----------------------------
# Make Prediction
# -----------------------------

prediction = model.predict(input_data)
weather_type = label_encoder.inverse_transform(prediction)

print("\nSensor Values:")
print("Temperature:", temperature)
print("Humidity:", humidity)
print("Precipitation:", precipitation)
print("UV Index:", uv_index)

print("\nPredicted Weather:", weather_type[0])
