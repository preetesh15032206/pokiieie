import pandas as pd
import numpy as np
import os

def build_dataset(input_file="weather_log.csv", output_file="forecast_dataset.csv"):
    if not os.path.exists(input_file):
        print(f"{input_file} not found. Generating advanced dummy data...")
        # Create a more realistic time-series dummy dataset
        rows = 500
        data = {
            'Temperature': np.random.uniform(20, 35, rows),
            'Humidity': np.random.uniform(30, 95, rows),
            'Precipitation (%)': np.random.uniform(0, 100, rows),
            'UV Index': np.random.uniform(0, 12, rows),
            'Pressure': np.random.uniform(990, 1020, rows),
            'Condition': np.random.choice(['Sunny', 'Cloudy', 'Rainy'], rows)
        }
        df = pd.DataFrame(data)
        df.to_csv(input_file, index=False)
    else:
        df = pd.read_csv(input_file)

    # 2 hours ahead = 24 rows
    shift = 24
    
    forecast_df = df.copy()
    if len(df) > shift:
        forecast_df['Target_Condition'] = df['Condition'].shift(-shift)
    else:
        forecast_df['Target_Condition'] = df['Condition']
    
    forecast_df = forecast_df.dropna(subset=['Target_Condition'])
    forecast_df.to_csv(output_file, index=False)
    print(f"Dataset built: {output_file}")

if __name__ == "__main__":
    build_dataset()
