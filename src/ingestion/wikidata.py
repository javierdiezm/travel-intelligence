import httpx
from dotenv import load_dotenv
import os
import math
from pathlib import Path
import pandas as pd

# ======================================================
# Configuración
# ======================================================
load_dotenv()

email = os.getenv(
    'WIKIDATA_USER_AGENT_EMAIL'
)

url = 'https://www.wikidata.org/w/api.php'

headers = {
    'User-Agent': f'travel-intelligence/0.1 (contact: {email})',
    'Accept': 'application/sparql-results+json'
}

# ======================================================
# Funciones auxiliares
# ======================================================
def calculate_distance_km(
    latitude_1,
    longitude_1,
    latitude_2,
    longitude_2
):
    """
    Calculate the great-circle distance between
    two geographic coordinates using the Haversine formula.
    """

    lat1 = math.radians(latitude_1)
    lat2 = math.radians(latitude_2)

    delta_lat = math.radians(
        latitude_2 - latitude_1
    )

    delta_lon = math.radians(
        longitude_2 - longitude_1
    )

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.asin(
        math.sqrt(a)
    )

    earth_radius_km = 6371

    return earth_radius_km * c

# ======================================================
# Wikidata country search
# ======================================================
def find_wikidata_country(country):
    """
    Find the Wikidata ID for a country name.
    """

    params = {
        'action': 'wbsearchentities',
        'search': country,
        'language': 'en',
        'format': 'json',
        'limit': 5
    }

    response = httpx.get(
        url,
        params=params,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    if not data.get('search'):
        return None

    return data['search'][0]['id']

# ======================================================
# Wikidata destination matching
# ======================================================
def find_wikidata_destination(
    city,
    country,
    latitude,
    longitude,
    manual_wikidata_id=None
):
    """
    Find the most likely Wikidata entity for a destination.

    Matching process:
    1. Use manual Wikidata ID when explicitly provided.
    2. Otherwise search candidates by destination name.
    3. Retrieve structured data for candidates.
    4. Filter candidates by country.
    5. Filter candidates without coordinates.
    6. Calculate geographic distance.
    7. Select the closest candidate.
    8. Extract useful destination information.
    """

    print(
        f'\nSearching: {city}, {country}'
    )

    # --------------------------------------------------
    # Manual Wikidata override
    # --------------------------------------------------
    if manual_wikidata_id is not None:

        print(
            f'Manual Wikidata ID: '
            f'{manual_wikidata_id}'
        )

        entity_params = {
            'action': 'wbgetentities',
            'ids': manual_wikidata_id,
            'format': 'json',
            'props': 'labels|descriptions|claims',
            'languages': 'en'
        }

        response = httpx.get(
            url,
            params=entity_params,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        entities_data = response.json()

        entity = entities_data.get(
            'entities',
            {}
        ).get(
            manual_wikidata_id
        )

        if entity is None:
            print(
                f'Wikidata entity not found: '
                f'{manual_wikidata_id}'
            )
            return None

        best_wikidata_id = manual_wikidata_id

    else:

        # --------------------------------------------------
        # 1. Find country Wikidata ID
        # --------------------------------------------------
        country_id = find_wikidata_country(
            country
        )

        if country_id is None:
            print(f'Country not found: {country}')
            return None

        print(f'Country Wikidata ID: {country_id}')

        # --------------------------------------------------
        # 2. Search destination candidates
        # --------------------------------------------------
        search_params = {
            'action': 'wbsearchentities',
            'search': city,
            'language': 'en',
            'format': 'json',
            'limit': 10
        }

        response = httpx.get(
            url,
            params=search_params,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        wikidata_ids = [
            result['id']
            for result in data.get(
                'search',
                []
            )
        ]

        if not wikidata_ids:

            print(
                f'No Wikidata candidates found: '
                f'{city}'
            )

            return None

        print(
            f'Candidates found: '
            f'{len(wikidata_ids)}'
        )

        # --------------------------------------------------
        # 3. Retrieve structured data
        # --------------------------------------------------
        entity_params = {
            'action': 'wbgetentities',
            'ids': '|'.join(wikidata_ids),
            'format': 'json',
            'props': 'labels|descriptions|claims',
            'languages': 'en'
        }

        entity_response = httpx.get(
            url,
            params=entity_params,
            headers=headers,
            timeout=30
        )

        entity_response.raise_for_status()

        entities_data = (
            entity_response.json()
        )

        # --------------------------------------------------
        # 4. Filter candidates
        # --------------------------------------------------
        candidates = []

        for wikidata_id, entity in (
            entities_data
            .get('entities', {})
            .items()
        ):

            claims = entity.get('claims',{})

            # Candidate must have country
            if 'P17' not in claims:
                continue

            # Candidate must have coordinates
            if 'P625' not in claims:
                continue

            # --------------------------------------------------
            # Country
            # --------------------------------------------------
            candidate_country_id = (
                claims['P17'][0]
                .get('mainsnak', {})
                .get('datavalue', {})
                .get('value', {})
                .get('id')
            )

            if (candidate_country_id != country_id):
                continue

            # --------------------------------------------------
            # Coordinates
            # --------------------------------------------------
            coordinate = (
                claims['P625'][0]
                .get('mainsnak', {})
                .get('datavalue', {})
                .get('value', {})
            )

            candidate_latitude = (
                coordinate.get('latitude')
            )

            candidate_longitude = (
                coordinate.get('longitude')
            )

            if (
                candidate_latitude is None
                or candidate_longitude is None
            ):
                continue

            # --------------------------------------------------
            # Distance
            # --------------------------------------------------
            distance = calculate_distance_km(
                latitude,
                longitude,
                candidate_latitude,
                candidate_longitude
            )

            candidates.append({
                'wikidata_id':
                    wikidata_id,
                'distance_km':
                    distance
            })

        # --------------------------------------------------
        # 5. Check candidates
        # --------------------------------------------------
        if not candidates:
            print(
                f'No valid candidates found: '
                f'{city}, {country}'
            )
            return None

        # --------------------------------------------------
        # 6. Select closest candidate
        # --------------------------------------------------
        best_candidate = min(
            candidates,
            key=lambda candidate:
            candidate['distance_km']
        )

        best_wikidata_id = (
            best_candidate[
                'wikidata_id'
            ]
        )

        entity = entities_data[
            'entities'
        ][best_wikidata_id]

    # ==================================================
    # Extract entity information
    # ==================================================

    # --------------------------------------------------
    # Label
    # --------------------------------------------------
    label = (
        entity
        .get('labels', {})
        .get('en', {})
        .get('value')
    )

    # --------------------------------------------------
    # Description
    # --------------------------------------------------
    description = (
        entity
        .get('descriptions', {})
        .get('en', {})
        .get('value')
    )

    # --------------------------------------------------
    # Population
    # --------------------------------------------------
    population = None

    population_claims = (
        entity
        .get('claims', {})
        .get('P1082', [])
    )

    if population_claims:

        population_value = (
            population_claims[0]
            .get('mainsnak', {})
            .get('datavalue', {})
            .get('value', {})
            .get('amount')
        )

        if population_value is not None:

            population = int(
                float(population_value)
            )

    # --------------------------------------------------
    # Wikidata coordinates
    # --------------------------------------------------
    coordinate = (
        entity
        .get('claims', {})
        .get('P625', [{}])[0]
        .get('mainsnak', {})
        .get('datavalue', {})
        .get('value', {})
        or {}
    )

    wikidata_latitude = (
        coordinate.get('latitude')
    )

    wikidata_longitude = (
        coordinate.get('longitude')
    )

    # --------------------------------------------------
    # Distance
    # --------------------------------------------------
    if manual_wikidata_id is not None:
        distance = calculate_distance_km(
            latitude,
            longitude,
            wikidata_latitude,
            wikidata_longitude
        )

    else:
        distance = best_candidate[
            'distance_km'
        ]

    # --------------------------------------------------
    # Build result
    # --------------------------------------------------
    result = {
        'wikidata_id':
            best_wikidata_id,
        'wikidata_label':
            label,
        'description':
            description,
        'population':
            population,
        'wikidata_latitude':
            wikidata_latitude,
        'wikidata_longitude':
            wikidata_longitude,
        'distance_km':
            distance
    }

    print(
        f"Matched: "
        f"{best_wikidata_id} | "
        f"{label} | "
        f"{round(distance, 3)} km"
    )

    return result

# ======================================================
# Main pipeline
# ======================================================
destinations = pd.read_csv('data/raw/destinations.csv')

# ======================================================
# Manual Wikidata overrides
# ======================================================
manual_matches = {
    'DPS': 'Q4648'
}

# ======================================================
# Process destinations
# ======================================================
results = []

for _, destination in (
    destinations.iterrows()
):

    destination_id = (
        destination['destination_id']
    )

    manual_wikidata_id = (
        manual_matches.get(
            destination_id
        )
    )

    result = find_wikidata_destination(
        city=destination['city'],
        country=destination['country'],
        latitude=destination['latitude'],
        longitude=destination['longitude'],
        manual_wikidata_id=manual_wikidata_id
    )

    if result is None:

        print(
            f"WARNING: Could not match "
            f"{destination_id}"
        )

        results.append({
            'destination_id':
                destination_id,
            'city':
                destination['city'],
            'country':
                destination['country'],
            'wikidata_id':
                None,
            'wikidata_label':
                None,
            'description':
                None,
            'population':
                None,
            'wikidata_latitude':
                None,
            'wikidata_longitude':
                None,
            'distance_km':
                None
        })
        continue

    results.append({
        'destination_id':
            destination_id,

        'city':
            destination['city'],

        'country':
            destination['country'],

        **result
    })


# ======================================================
# Create output dataframe
# ======================================================
wikidata_df = pd.DataFrame(
    results
)


# ======================================================
# Save results
# ======================================================
output_dir = Path('data/reference')

output_dir.mkdir(parents=True, exist_ok=True)

output_file = (output_dir / 'destination_sources.csv')

wikidata_df.to_csv(output_file, index=False)