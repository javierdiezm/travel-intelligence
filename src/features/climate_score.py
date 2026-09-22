import pandas as pd


def calculate_temperature_score(temperature: float, preference: str) -> float:

    # ==================================================
    # COLD
    # ==================================================
    if preference == 'cold':
        if temperature <= 5:
            distance = 5 - temperature
            score = 100 - (distance * 3)
        elif temperature <= 15:
            score = 100
        else:
            distance = temperature - 15
            score = 100 - (distance * 8)

    # ==================================================
    # COOL
    # ==================================================
    elif preference == 'cool':
        if temperature < 5:
            distance = 5 - temperature
            score = 50 - (distance * 5)
        elif temperature < 12:
            score = 50 + ((temperature - 5) / 7 * 40)
        elif temperature <= 15:
            score = 90 + ((temperature - 12) / 3 * 10)
        elif temperature <= 18:
            score = 100
        elif temperature <= 20:
            score = 100 - ((temperature - 18) / 2 * 10)
        else:
            score = max(0, 90 - ((temperature - 20) * 10))

    # ==================================================
    # PLEASANT
    # ==================================================
    elif preference == 'pleasant':
        if temperature <= 5:
            score = max(0, 10 - ((5 - temperature) * 2))
        elif temperature <= 10:
            score = 10 + ((temperature - 5) / 5 * 25)
        elif temperature <= 15:
            score = 35 + ((temperature - 10) / 5 * 30)
        elif temperature <= 18:
            score = 65 + ((temperature - 15) / 3 * 17)
        elif temperature <= 20:
            score = 82 + ((temperature - 18) / 2 * 10)
        elif temperature <= 22:
            score = 92 + ((temperature - 20) / 2 * 8)
        elif temperature <= 23:
            score = 100
        elif temperature <= 25:
            score = 100 - ((temperature - 23) / 2 * 10)
        elif temperature <= 27:
            score = 90 - ((temperature - 25) / 2 * 18)
        elif temperature <= 30:
            score = 72 - ((temperature - 27) / 3 * 24)
        elif temperature <= 35:
            score = 48 - ((temperature - 30) / 5 * 40)
        else:
            score = max(0, 8 - ((temperature - 35) * 1.6))

    # ==================================================
    # WARM
    # ==================================================
    elif preference == 'warm':
        if temperature <= 15:
            score = max(0, 10 - ((15 - temperature) * 2))
        elif temperature <= 18:
            score = 10 + ((temperature - 15) / 3 * 15)
        elif temperature <= 20:
            score = 25 + ((temperature - 18) / 2 * 15)
        elif temperature <= 22:
            score = 40 + ((temperature - 20) / 2 * 20)
        elif temperature <= 24:
            score = 60 + ((temperature - 22) / 2 * 20)
        elif temperature <= 26:
            score = 80 + ((temperature - 24) / 2 * 15)
        elif temperature <= 28:
            score = 100
        elif temperature <= 30:
            score = 100 - ((temperature - 28) / 2 * 10)
        elif temperature <= 32:
            score = 90 - ((temperature - 30) / 2 * 15)
        elif temperature <= 35:
            score = 75 - ((temperature - 32) / 3 * 30)
        elif temperature <= 38:
            score = 45 - ((temperature - 35) / 3 * 30)
        else:
            score = max(0, 15 - ((temperature - 38) * 7.5))

    # ==================================================
    # VERY WARM
    # ==================================================
    elif preference == 'very_warm':
        if temperature <= 20:
            score = max(0, 5 - ((20 - temperature) * 1))
        elif temperature <= 22:
            score = 5 + ((temperature - 20) / 2 * 10)
        elif temperature <= 24:
            score = 15 + ((temperature - 22) / 2 * 15)
        elif temperature <= 26:
            score = 30 + ((temperature - 24) / 2 * 20)
        elif temperature <= 28:
            score = 50 + ((temperature - 26) / 2 * 25)
        elif temperature <= 30:
            score = 75 + ((temperature - 28) / 2 * 15)
        elif temperature <= 32:
            score = 90 + ((temperature - 30) / 2 * 10)
        elif temperature <= 34:
            score = 100
        elif temperature <= 35:
            score = 98
        elif temperature <= 37:
            score = 98 - ((temperature - 35) / 2 * 8)
        elif temperature <= 40:
            score = 90 - ((temperature - 37) / 3 * 20)
        elif temperature <= 42:
            score = 70 - ((temperature - 40) / 2 * 25)
        elif temperature <= 45:
            score = 45 - ((temperature - 42) / 3 * 35)
        else:
            score = max(0, 10 - ((temperature - 45) * 5))

    else:
        raise ValueError(f'Temperature preference not implemented yet: {preference}')

    return max(0, min(100, score))


def calculate_rain_score(rainy_days: float, precipitation: float, preference: str) -> float:

    if preference not in ['indifferent', 'low', 'very_low']:
        raise ValueError(f'Invalid rain preference: {preference}')

    if preference == 'indifferent':
        return 100.0

    # ==================================================
    # SCORE DE PRECIPITACIÓN
    # ==================================================
    if preference == 'low':
        if precipitation <= 40:
            precipitation_score = 100
        elif precipitation <= 100:
            precipitation_score = 100 - ((precipitation - 40) / 60 * 20)
        elif precipitation <= 200:
            precipitation_score = 80 - ((precipitation - 100) / 100 * 40)
        else:
            precipitation_score = max(10, 40 - ((precipitation - 200) / 100 * 15))

    elif preference == 'very_low':
        if precipitation <= 20:
            precipitation_score = 100
        elif precipitation <= 60:
            precipitation_score = 100 - ((precipitation - 20) / 40 * 30)
        elif precipitation <= 120:
            precipitation_score = 70 - ((precipitation - 60) / 60 * 40)
        else:
            precipitation_score = max(5, 30 - ((precipitation - 120) / 80 * 25))

    # ==================================================
    # SCORE DE FRECUENCIA
    # ==================================================
    if rainy_days <= 5:
        rainy_days_score = 100
    elif rainy_days <= 10:
        rainy_days_score = 100 - ((rainy_days - 5) / 5 * 15)
    elif rainy_days <= 15:
        rainy_days_score = 85 - ((rainy_days - 10) / 5 * 20)
    elif rainy_days <= 20:
        rainy_days_score = 65 - ((rainy_days - 15) / 5 * 25)
    else:
        rainy_days_score = max(20, 40 - ((rainy_days - 20) * 4))

    # ==================================================
    # SCORE FINAL
    # ==================================================
    score = (precipitation_score * 0.7) + (rainy_days_score * 0.3)
    return max(0, min(100, score))


def calculate_sunshine_score(sunshine_hours: float, preference: str) -> float:

    if preference not in ['indifferent', 'high', 'very_high']:
        raise ValueError(f'Invalid sunshine preference: {preference}')

    if preference == 'indifferent':
        return 100.0

    # ==================================================
    # HIGH
    # ==================================================
    if preference == 'high':
        if sunshine_hours <= 3:
            score = 0
        elif sunshine_hours <= 4:
            score = 0 + ((sunshine_hours - 3) / 1 * 20)
        elif sunshine_hours <= 5:
            score = 20 + ((sunshine_hours - 4) / 1 * 20)
        elif sunshine_hours <= 6:
            score = 40 + ((sunshine_hours - 5) / 1 * 20)
        elif sunshine_hours <= 7:
            score = 60 + ((sunshine_hours - 6) / 1 * 15)
        elif sunshine_hours <= 8:
            score = 75 + ((sunshine_hours - 7) / 1 * 10)
        elif sunshine_hours <= 9:
            score = 85 + ((sunshine_hours - 8) / 1 * 7)
        elif sunshine_hours <= 10:
            score = 92 + ((sunshine_hours - 9) / 1 * 5)
        elif sunshine_hours <= 11:
            score = 97 + ((sunshine_hours - 10) / 1 * 3)
        else:
            score = 100

    # ==================================================
    # VERY HIGH
    # ==================================================
    elif preference == 'very_high':
        if sunshine_hours <= 3:
            score = 0
        elif sunshine_hours <= 4:
            score = 0 + ((sunshine_hours - 3) / 1 * 10)
        elif sunshine_hours <= 5:
            score = 10 + ((sunshine_hours - 4) / 1 * 15)
        elif sunshine_hours <= 6:
            score = 25 + ((sunshine_hours - 5) / 1 * 15)
        elif sunshine_hours <= 7:
            score = 40 + ((sunshine_hours - 6) / 1 * 15)
        elif sunshine_hours <= 8:
            score = 55 + ((sunshine_hours - 7) / 1 * 15)
        elif sunshine_hours <= 9:
            score = 70 + ((sunshine_hours - 8) / 1 * 12)
        elif sunshine_hours <= 10:
            score = 82 + ((sunshine_hours - 9) / 1 * 10)
        elif sunshine_hours <= 11:
            score = 92 + ((sunshine_hours - 10) / 1 * 6)
        elif sunshine_hours <= 12:
            score = 98 + ((sunshine_hours - 11) / 1 * 2)
        else:
            score = 100

    return max(0, min(100, score))


def calculate_wind_score(wind_speed: float, preference: str) -> float:

    if preference not in ['indifferent', 'low', 'very_low']:
        raise ValueError(f'Invalid wind preference: {preference}')

    if preference == 'indifferent':
        return 100.0

    # ==================================================
    # LOW
    # ==================================================
    if preference == 'low':
        if wind_speed <= 10:
            score = 100
        elif wind_speed <= 15:
            score = 100 - ((wind_speed - 10) / 5 * 5)
        elif wind_speed <= 20:
            score = 95 - ((wind_speed - 15) / 5 * 10)
        elif wind_speed <= 25:
            score = 85 - ((wind_speed - 20) / 5 * 10)
        elif wind_speed <= 30:
            score = 75 - ((wind_speed - 25) / 5 * 15)
        elif wind_speed <= 35:
            score = 60 - ((wind_speed - 30) / 5 * 15)
        elif wind_speed <= 40:
            score = 45 - ((wind_speed - 35) / 5 * 15)
        elif wind_speed <= 45:
            score = 30 - ((wind_speed - 40) / 5 * 10)
        elif wind_speed <= 50:
            score = 20 - ((wind_speed - 45) / 5 * 10)
        elif wind_speed <= 55:
            score = 10 - ((wind_speed - 50) / 5 * 10)
        else:
            score = 0

    # ==================================================
    # VERY LOW
    # ==================================================
    elif preference == 'very_low':
        if wind_speed <= 8:
            score = 100
        elif wind_speed <= 10:
            score = 100 - ((wind_speed - 8) / 2 * 5)
        elif wind_speed <= 15:
            score = 95 - ((wind_speed - 10) / 5 * 10)
        elif wind_speed <= 20:
            score = 85 - ((wind_speed - 15) / 5 * 15)
        elif wind_speed <= 25:
            score = 70 - ((wind_speed - 20) / 5 * 20)
        elif wind_speed <= 30:
            score = 50 - ((wind_speed - 25) / 5 * 20)
        elif wind_speed <= 35:
            score = 30 - ((wind_speed - 30) / 5 * 15)
        elif wind_speed <= 40:
            score = 15 - ((wind_speed - 35) / 5 * 10)
        elif wind_speed <= 45:
            score = 5 - ((wind_speed - 40) / 5 * 5)
        else:
            score = 0

    return max(0, min(100, score))


def calculate_climate_score(row: pd.Series, preferences: dict) -> float:

    # ==================================================
    # PESOS DINÁMICOS
    # ==================================================
    weights = calculate_dynamic_weights(preferences)
    scores = []

    # ==================================================
    # TEMPERATURA
    # ==================================================
    if preferences['temperature'] != 'indifferent':
        temperature_score = calculate_temperature_score(row['temperature_mean'], preferences['temperature'])
        scores.append(temperature_score * weights['temperature'])

    # ==================================================
    # LLUVIA
    # ==================================================
    if preferences['rain'] != 'indifferent':
        rain_score = calculate_rain_score(
            row['rainy_days_avg'],
            row['precipitation_monthly_avg'],
            preferences['rain']
        )
        scores.append(rain_score * weights['rain'])

    # ==================================================
    # SOL
    # ==================================================
    if preferences['sunshine'] != 'indifferent':
        sunshine_score = calculate_sunshine_score(row['sunshine_hours_avg'], preferences['sunshine'])
        scores.append(sunshine_score * weights['sunshine'])

    # ==================================================
    # VIENTO
    # ==================================================
    if preferences['wind'] != 'indifferent':
        wind_score = calculate_wind_score(row['wind_speed_max_avg'], preferences['wind'])
        scores.append(wind_score * weights['wind'])

    return sum(scores)


def calculate_dynamic_weights(preferences: dict) -> dict:

    base_weights = {
        'temperature': 0.40,
        'rain': 0.30,
        'sunshine': 0.20,
        'wind': 0.10
    }

    active_variables = []

    for variable in base_weights:
        if preferences[variable] != 'indifferent':
            active_variables.append(variable)

    # ==================================================
    # TODAS INDIFERENTES
    # ==================================================
    if not active_variables:
        equal_weight = 1 / len(base_weights)
        return {variable: equal_weight for variable in base_weights}

    # ==================================================
    # REDISTRIBUCIÓN DE PESOS
    # ==================================================
    active_weight = sum(base_weights[variable] for variable in active_variables)

    dynamic_weights = {}

    for variable in base_weights:
        if variable in active_variables:
            dynamic_weights[variable] = base_weights[variable] / active_weight
        else:
            dynamic_weights[variable] = 0.0

    return dynamic_weights


if __name__ == '__main__':

    import pandas as pd

    climate = pd.read_csv('data/processed/destination_climate.csv')

    preference_profiles = [

        {
            'name': 'Perfil equilibrado',
            'temperature': 'pleasant',
            'rain': 'low',
            'sunshine': 'high',
            'wind': 'low'
        },

        {
            'name': 'Perfil tropical',
            'temperature': 'very_warm',
            'rain': 'very_low',
            'sunshine': 'very_high',
            'wind': 'low'
        },

        {
            'name': 'Perfil fresco',
            'temperature': 'cool',
            'rain': 'indifferent',
            'sunshine': 'indifferent',
            'wind': 'indifferent'
        }

    ]

    september = climate[climate['month'] == 9].copy()

    for profile in preference_profiles:

        preferences = {key: value for key, value in profile.items() if key != 'name'}

        results = []

        for _, row in september.iterrows():

            temperature_score = calculate_temperature_score(row['temperature_mean'], preferences['temperature'])

            if preferences['rain'] != 'indifferent':
                rain_score = calculate_rain_score(
                    row['rainy_days_avg'],
                    row['precipitation_monthly_avg'],
                    preferences['rain']
                )
            else:
                rain_score = 100.0

            if preferences['sunshine'] != 'indifferent':
                sunshine_score = calculate_sunshine_score(row['sunshine_hours_avg'], preferences['sunshine'])
            else:
                sunshine_score = 100.0

            if preferences['wind'] != 'indifferent':
                wind_score = calculate_wind_score(row['wind_speed_max_avg'], preferences['wind'])
            else:
                wind_score = 100.0

            climate_score = calculate_climate_score(row, preferences)

            results.append({
                'destination_id': row['destination_id'],
                'city': row['city'],
                'temperature_score': temperature_score,
                'rain_score': rain_score,
                'sunshine_score': sunshine_score,
                'wind_score': wind_score,
                'climate_score': climate_score
            })

        results = pd.DataFrame(results)

        results = results.sort_values('climate_score', ascending=False)

        print('\n' + '=' * 90)
        print(profile['name'].upper())
        print('=' * 90)

        print('\nPreferences:')
        print(preferences)

        print('\nResults:')

        print(
            results.to_string(
                index=False,
                float_format=lambda x: f'{x:.2f}'
            )
        )