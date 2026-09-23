import pandas as pd

# ======================================================
# Cargar datos
# ======================================================
destinations = pd.read_csv('data/raw/destinations.csv')

climate = pd.read_csv('data/processed/climate_features.csv')

# ======================================================
# Merge datasets
# ======================================================
destination_climate = destinations.merge(
    climate,
    on='destination_id',
    how='left'
)

# ======================================================
# Validation
# ======================================================
print('\n' + '=' * 60)
print('DESTINATION FEATURES')
print('=' * 60)

print(f'\nRows: {len(destination_climate)}')

print(f'Columns: {len(destination_climate.columns)}')

print('\nColumns:')
print(destination_climate.columns.tolist())

print('\nNull values:')
print(destination_climate.isnull().sum())

print('\nPreview:')
print(destination_climate.head(20).to_string(index=False))

# ======================================================
# Guardar dataset
# ======================================================
output_file = ('data/processed/destination_climate.csv')

destination_climate.to_csv(output_file, index=False)

print(f'\nDataset saved to: {output_file}')