import json
from pathlib import Path
import pandas as pd

weather_files = Path('data/raw/weather_historical').glob('*/*.json')

weather_data = []

for file in weather_files:

    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    daily = data['daily']

    df = pd.DataFrame({
        'destination_id': file.stem,
        'date': daily['time'],
        'temperature_mean': daily['temperature_2m_mean'],
        'temperature_max': daily['temperature_2m_max'],
        'temperature_min': daily['temperature_2m_min'],
        'precipitation': daily['precipitation_sum'],
        'sunshine_duration': daily['sunshine_duration'],
        'wind_speed_max': daily['wind_speed_10m_max']
    })

    weather_data.append(df)

weather_df = pd.concat(weather_data, ignore_index=True)
weather_df['date'] = pd.to_datetime(weather_df['date'])
weather_df['sunshine_hours'] = weather_df['sunshine_duration'] / 3600
weather_df['month'] = weather_df['date'].dt.month
weather_df['year'] = weather_df['date'].dt.year

monthly_precipitation = (
    weather_df
    .groupby(['destination_id', 'year', 'month'])
    ['precipitation']
    .sum()
    .reset_index()
)

monthly_precipitation = (
    monthly_precipitation
    .groupby(['destination_id', 'month'])['precipitation']
    .mean()
    .reset_index()
)

rainy_days = (
    weather_df
    .assign(rainy_day=weather_df['precipitation'] > 1)
    .groupby(['destination_id', 'year', 'month'])['rainy_day']
    .sum()
    .reset_index()
)

rainy_days = (
    rainy_days
    .groupby(['destination_id', 'month'])['rainy_day']
    .mean()
    .reset_index()
)

monthly_weather = (
    weather_df
    .groupby(['destination_id', 'month'])
    .agg({
        'temperature_mean': 'mean',
        'temperature_max': 'mean',
        'temperature_min': 'mean',
        'precipitation': ['mean', 'sum'],
        'sunshine_hours': 'mean',
        'wind_speed_max': 'mean'
    })
    .reset_index()
)

monthly_weather.columns = [
    'destination_id',
    'month',
    'temperature_mean',
    'temperature_max_avg',
    'temperature_min_avg',
    'precipitation_daily_avg',
    'precipitation_monthly_total',
    'sunshine_hours_avg',
    'wind_speed_max_avg'
]

monthly_weather = monthly_weather.drop(
    columns=['precipitation_monthly_total']
)

monthly_weather = monthly_weather.merge(
    monthly_precipitation,
    on=['destination_id', 'month'],
    how='left'
)

monthly_weather = monthly_weather.rename(
    columns={'precipitation': 'precipitation_monthly_avg'}
)

monthly_weather = monthly_weather.merge(
    rainy_days,
    on=['destination_id', 'month'],
    how='left'
)

monthly_weather = monthly_weather.rename(
    columns={'rainy_day': 'rainy_days_avg'}
)

output_file = Path('data/processed/weather_historical_daily.csv')
weather_df.to_csv(output_file, index=False)

output_file = Path('data/processed/weather_historical_monthly.csv')
monthly_weather.to_csv(output_file, index=False)

print(f"Dataset mensual guardado en: {output_file}")
print(f"Shape: {monthly_weather.shape}")

print(
    monthly_weather
    .groupby('destination_id')['month']
    .count()
)