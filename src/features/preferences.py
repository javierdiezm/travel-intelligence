# ======================================================
# Preferencias climáticas
# ======================================================
TEMPERATURE_OPTIONS = [
    'indifferent',
    'cold',
    'cool',
    'pleasant',
    'warm',
    'very_warm'
]

RAIN_OPTIONS = [
    'indifferent',
    'low',
    'very_low'
]

SUNSHINE_OPTIONS = [
    'indifferent',
    'high',
    'very_high'
]

WIND_OPTIONS = [
    'indifferent',
    'low',
    'very_low'
]

def validate_preferences(
    temperature: str,
    rain: str,
    sunshine: str,
    wind: str
) -> dict:

    if temperature not in TEMPERATURE_OPTIONS:
        raise ValueError(
            f'Invalid temperature preference: {temperature}'
        )

    if rain not in RAIN_OPTIONS:
        raise ValueError(
            f'Invalid rain preference: {rain}'
        )

    if sunshine not in SUNSHINE_OPTIONS:
        raise ValueError(
            f'Invalid sunshine preference: {sunshine}'
        )

    if wind not in WIND_OPTIONS:
        raise ValueError(
            f'Invalid wind preference: {wind}'
        )

    return {
        'temperature': temperature,
        'rain': rain,
        'sunshine': sunshine,
        'wind': wind
    }