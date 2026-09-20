import json
from pathlib import Path
import pandas as pd

weather_files = Path('data/raw/weather/').glob('*.json')

weather_data = []

for file in weather_files:
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)

        daily = data['daily']
        df = pd.DataFrame({
            'destination_id': file.stem,
            'date': daily['time'],
            'temperature_max': daily['temperature_2m_max'],
            'temperature_min': daily['temperature_2m_min'],
            'precipitation': daily['precipitation_sum'],
            'sunshine_duration': daily['sunshine_duration']
        })
        df['date'] = pd.to_datetime(df['date'])

    weather_data.append(df)

weather_df = pd.concat(weather_data, ignore_index=True)

output_file = Path('data/processed/weather_daily.csv')
weather_df.to_csv(output_file, index=False)

print(f"Dataset guardado en: {output_file}")

print(weather_df.isna().sum())
print(weather_df.duplicated(subset=['destination_id', 'date']).sum())

print(weather_df.groupby('destination_id').size())