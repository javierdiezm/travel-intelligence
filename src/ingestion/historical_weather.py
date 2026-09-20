import httpx
import pandas as pd
from pathlib import Path
import json
import time

def get_with_retry(url, params, max_retries=5):
    for attemp in range(max_retries):
        response = httpx.get(url, params=params)

        if response.status_code == 200:
            return response

        if response.status_code == 429:
            wait_time = 5 * (attemp + 1)

            print(
                f"429 Too Many Requests. "
                f"Esperando {wait_time} segundos..."
            )

            time.sleep(wait_time)
            continue

        response.raise_for_status()
    raise Exception('No se puedo obtener la respuesta después de varios intentos.')

url = 'https://archive-api.open-meteo.com/v1/archive'

destinations = pd.read_csv('data/raw/destinations.csv')

output_dir = Path('data/raw/weather_historical')
output_dir.mkdir(parents=True, exist_ok=True)

for year in range(2015, 2026):
    start_date = f'{year}-01-01'
    end_date = f'{year}-12-31'

    output_dir = Path(f'data/raw/weather_historical/{year}')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for _, destination in destinations.iterrows():

        output_file = output_dir / f"{destination['destination_id']}.json"
        
        if output_file.exists():
            print(f"{year} | {destination['destination_id']} | ya existe")
            continue

        params = {
            'latitude': destination['latitude'],
            'longitude': destination['longitude'],
            'start_date': start_date,
            'end_date': end_date,
            'daily': [
                'temperature_2m_mean',
                'temperature_2m_max',
                'temperature_2m_min',
                'precipitation_sum',
                'sunshine_duration',
                'wind_speed_10m_max'
            ],
            'timezone': 'auto'
        }

        response = get_with_retry(url, params)
        print(f"Destination: {destination['destination_id']} | Status: {response.status_code}")

        data = response.json()

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        print(f"{destination['destination_id']} | guardado")

        time.sleep(2)