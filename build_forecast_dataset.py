import pandas as pd
import numpy as np
import os

def build_dataset(input_file="weather_log.csv", output_file="forecast_dataset.csv"):
    # If weather_log.csv doesn't exist, create a dummy one with proper columns
    if not os.path.exists(input_file):
        print(f"{input_file} not found. Generating dummy data for training...")
        data = {
            'Temperature': np.random.uniform(20, 35, 200),
            'Humidity': np.random.uniform(30, 95, 200),
            'Precipitation (%)': np.random.uniform(0, 100, 200),
            'UV Index': np.random.uniform(0, 12, 200),
            'Pressure': np.random.uniform(990, 1020, 200),
            'Condition': np.random.choice(['Sunny', 'Cloudy', 'Rainy'], 200)
        }
        df = pd.DataFrame(data)
        df.to_csv(input_file, index=False)
    else:
        df = pd.read_csv(input_file)

    # 2 hours ahead = 24 rows
    shift = 24
    
    forecast_df = df.copy()
    # If we don't have enough rows for a real shift, we'll just use the current condition for dummy training
    if len(df) <= shift:
        forecast_df['Target_Condition'] = df['Condition']
    else:
        forecast_df['Target_Condition'] = df['Condition'].shift(-shift)
    
    forecast_df = forecast_df.dropna(subset=['Target_Condition'])
    forecast_df.to_csv(output_file, index=False)
    print(f"Dataset built: {output_file}")

if __name__ == "__main__":
    build_dataset()
