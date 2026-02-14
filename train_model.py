import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv("weather_classification_data.csv")

# Select only required columns
df = df[["Temperature", "Humidity", "Precipitation (%)", "UV Index", "Weather Type"]]

# Encode target labels
label_encoder = LabelEncoder()
df["Weather Type"] = label_encoder.fit_transform(df["Weather Type"])

# Features and target
X = df[["Temperature", "Humidity", "Precipitation (%)", "UV Index"]]
y = df["Weather Type"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Test accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", accuracy)

# Save model and encoder
joblib.dump(model, "weather_model.pkl")
joblib.dump(label_encoder, "label_encoder.pkl")

print("Model saved successfully!")
