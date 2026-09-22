import pandas as pd
from datetime import date

from trip_dates import get_trip_months

# ======================================================
# Configuración
# ======================================================
CLIMATE_FILE = 'data/processed/destination_climate.csv'

# ======================================================
# Obtener clima del viaje
# ======================================================
def get_climate_for_trip(
    start_date: date,
    end_date: date
) -> pd.DataFrame:

    months = get_trip_months(
        start_date,
        end_date
    )

    climate = pd.read_csv(CLIMATE_FILE)

    climate_for_trip = climate[
        climate['month'].isin(months)
    ].copy()

    return climate_for_trip

# ======================================================
# Test
# ======================================================
if __name__ == '__main__':

    start_date = date(2027, 9, 6)
    end_date = date(2027, 9, 18)

    climate = get_climate_for_trip(start_date, end_date)

    print('\n' + '=' * 60)
    print('CLIMATE FOR TRIP')
    print('=' * 60)

    print(f'\nTrip: {start_date} → {end_date}')
    print(f'\nRows: {len(climate)}')
    print('\nClimate data:')

    print(
        climate[
            [
                'destination_id',
                'city',
                'country',
                'month',
                'temperature_mean',
                'precipitation_monthly_avg',
                'rainy_days_avg',
                'sunshine_hours_avg',
                'temperature_score',
                'rain_score',
                'sunshine_score',
                'wind_score'
            ]
        ].to_string(index=False)
    )