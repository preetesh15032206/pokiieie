import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

def train_forecast():
    try:
        df = pd.read_csv("forecast_dataset.csv")
        
        X = df[['Temperature', 'Humidity', 'Precipitation (%)', 'UV Index', 'Pressure']]
        y = df['Target_Condition']
        
        le = LabelEncoder()
        y_encoded = le.fit_transform(y)
        
        model = RandomForestClassifier(n_estimators=100)
        model.fit(X, y_encoded)
        
        joblib.dump(model, "forecast_model.pkl")
        joblib.dump(le, "forecast_encoder.pkl")
        
        print("Forecast model trained and saved.")
        
    except Exception as e:
        print(f"Training error: {e}")

if __name__ == "__main__":
    train_forecast()
