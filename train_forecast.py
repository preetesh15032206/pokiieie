import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

def train_models():
    try:
        df = pd.read_csv("forecast_dataset.csv")
        
        # 1. Current Weather Model (4 features)
        X1 = df[['Temperature', 'Humidity', 'Precipitation (%)', 'UV Index']]
        y1 = df['Condition']
        le1 = LabelEncoder()
        y1_enc = le1.fit_transform(y1)
        m1 = RandomForestClassifier(n_estimators=100)
        m1.fit(X1, y1_enc)
        joblib.dump(m1, "weather_model.pkl")
        joblib.dump(le1, "label_encoder.pkl")
        
        # 2. Forecast Model (5 features including Pressure)
        X2 = df[['Temperature', 'Humidity', 'Precipitation (%)', 'UV Index', 'Pressure']]
        y2 = df['Target_Condition']
        le2 = LabelEncoder()
        y2_enc = le2.fit_transform(y2)
        m2 = RandomForestClassifier(n_estimators=100)
        m2.fit(X2, y2_enc)
        joblib.dump(m2, "forecast_model.pkl")
        joblib.dump(le2, "forecast_encoder.pkl")
        
        print("All models trained and saved successfully.")
        
    except Exception as e:
        print(f"Training error: {e}")

if __name__ == "__main__":
    train_models()
