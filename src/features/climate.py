import pandas as pd

# =========================
# 1. Cargar datos
# =========================
weather = pd.read_csv(
    'data/processed/weather_historical_monthly.csv'
)

# =========================
# 2. Features temperatura
# =========================
weather['pleasant_temperature'] = (
    (weather['temperature_mean'] >= 18) &
    (weather['temperature_mean'] <= 28)
)

weather['temperature_distance'] = (
    weather['temperature_mean'] - 25
).abs()

weather['temperature_score'] = (
    100 - (weather['temperature_distance'] / 10 * 100)
).clip(0, 100)

# =========================
# 3. Features lluvia
# =========================
# limite 300mm
weather['rain_score'] = (
    100 - (weather['precipitation_monthly_avg'] / 300 * 100)
).clip(0, 100)

# =========================
# 4. Features sol
# =========================
# 12 horas al día de sol
weather['sunshine_score'] = (
    weather['sunshine_hours_avg'] / 12 * 100
).clip(0, 100)

# =========================
# 5. Features viento
# =========================
# Menos 10km/h es ideal, más de 30km/h es malo
weather['wind_score'] = (
    100 - ((weather['wind_speed_max_avg'] - 10) / 20 * 100)
).clip(0, 100)

print(
    weather[
        weather['destination_id'].isin(['MAD', 'BKK', 'REK', 'ZNZ', 'IPC'])
    ][
        [
            'destination_id',
            'month',
            'temperature_mean',
            'temperature_distance',
            'temperature_score'
        ]
    ].to_string(index=False)
)

# =========================
# 6. Guardar features clima
# =========================

output_file = 'data/processed/climate_features.csv'

weather.to_csv(
    output_file,
    index=False
)

print(f'Dataset guardado en: {output_file}')
print(f'Shape: {weather.shape}')

# =========================
# 7. Quality checks
# =========================
print('\nNull values:')
print(weather.isnull().sum())

print('\nMonths per destination:')
print(
    weather.groupby('destination_id')['month']
    .count()
)

print('\nDuplicate rows:')
print(weather.duplicated().sum())