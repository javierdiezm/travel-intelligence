import httpx
import json
from pathlib import Path
import pandas as pd

url = 'https://api.open-meteo.com/v1/forecast'

destinations = pd.read_csv('data/raw/destinations.csv')

output_dir = Path('data/raw/weather')
output_dir.mkdir(parents=True, exist_ok=True)

for _, destination in destinations.iterrows():

    params = {
        'latitude': destination['latitude'],
        'longitude': destination['longitude'],
        'daily': [
            'temperature_2m_max',
            'temperature_2m_min',
            'precipitation_sum',
            'sunshine_duration',
        ]
    }
    response = httpx.get(url, params=params)

    response.raise_for_status()

    print(f"Destination: {destination['destination_id']} | Status: {response.status_code}")

    output_file = output_dir / f"{destination['destination_id']}.json"

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(response.json(), f, indent=2)