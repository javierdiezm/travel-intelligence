# Travel Intelligence ✈️

Travel Intelligence es un proyecto de datos que intenta responder a una pregunta sencilla:

> **¿A dónde viajo según mis fechas, mi presupuesto y mis preferencias?**

Quiero construir un sistema de recomendación de viajes que combine distintos tipos de información (clima, precios, vuelos, alojamiento, actividades y características de cada destino) y que sus recomendaciones se puedan explicar, en lugar de depender de una única puntuación opaca.

El proyecto avanza por fases. Empiezo por la capa de datos y el análisis del clima, y más adelante pasaré a la inteligencia de destinos y al motor de recomendación.

---

## Estado del proyecto

**Fase actual:** pipeline de datos climáticos e ingeniería de variables

La primera versión del pipeline de clima ya funciona:

* Datos meteorológicos históricos de 2015 a 2025
* 10 destinos iniciales
* Agregación de diario a mensual
* Cálculo de días de lluvia
* Ingeniería de variables climáticas
* Comprobaciones básicas de calidad de datos
* Datasets procesados guardados en CSV

Siguiente paso: enriquecer los destinos con información geográfica y turística usando OpenStreetMap / Overpass y otras fuentes estructuradas.

---

## Destinos iniciales

El primer dataset tiene 10 destinos:

| ID  | Ciudad          | País                 |
| --- | --------------- | -------------------- |
| MAD | Madrid          | España               |
| NYC | Nueva York      | Estados Unidos       |
| ZNZ | Zanzíbar        | Tanzania             |
| MRU | Mauricio        | Mauricio             |
| MLE | Malé (Maldivas) | Maldivas             |
| PDC | Playa del Carmen| México               |
| SYD | Sídney          | Australia            |
| DPS | Bali            | Indonesia            |
| PUJ | Punta Cana      | República Dominicana |
| BKK | Bangkok         | Tailandia            |

La lista es pequeña a propósito. Prefiero montar bien el pipeline antes de escalarlo a un catálogo más grande.

---

## Arquitectura actual

El proyecto sigue un pipeline de datos sencillo:

```text
APIs externas
     │
     ▼
 Datos en bruto (raw)
     │
     ▼
   Ingesta
     │
     ▼
Transformación / limpieza
     │
     ▼
Datasets procesados
     │
     ▼
Ingeniería de variables
     │
     ▼
Motor de recomendación
     │
     ▼
API + aplicación web
```

A largo plazo quiero mantener separados los datos en bruto, los datos procesados y las variables derivadas, para poder reproducir cada etapa por su cuenta.

---

## Estructura del repositorio

```text
travel-intelligence/
│
├── data/
│   ├── raw/
│   │   ├── destinations.csv
│   │   ├── weather/
│   │   └── weather_historical/
│   │
│   └── processed/
│       ├── weather_daily.csv
│       ├── weather_historical_monthly.csv
│       └── climate_features.csv
│
├── src/
│   ├── ingestion/
│   │   ├── weather.py
│   │   └── historical_weather.py
│   │
│   ├── transformation/
│   │   ├── weather.py
│   │   └── historical_weather.py
│   │
│   └── features/
│       └── climate.py
│
├── notebooks/
│
├── tests/
│
├── requirements.txt
├── .gitignore
└── README.md
```

Los directorios de clima en bruto se generan al ejecutar la ingesta y no se suben al repositorio.

---

# Pipeline de clima

La primera parte del proyecto se centra en el clima histórico.

### Fuente de datos

Los datos históricos salen de la **Open-Meteo Historical Weather API**.

El periodo inicial es:

```text
2015 → 2025
```

Para cada destino se descargan observaciones diarias de:

* Temperatura media
* Temperatura máxima
* Temperatura mínima
* Precipitación
* Horas de sol
* Velocidad máxima del viento

Las respuestas originales de la API se guardan en local, de modo que el paso de transformación se puede repetir sin volver a llamar a la API.

---

## De datos diarios a clima mensual

El dataset en bruto contiene aproximadamente:

```text
10 destinos
×
11 años
×
365/366 días
```

Los datos diarios se transforman en un dataset climático mensual:

```text
10 destinos
×
12 meses
=
120 filas
```

El dataset mensual incluye:

* Temperatura media (promedio)
* Temperatura máxima media
* Temperatura mínima media
* Precipitación diaria media
* Precipitación mensual media
* Horas de sol diarias (promedio)
* Velocidad máxima del viento (promedio)
* Número medio de días de lluvia

### Días de lluvia

Por ahora, un día de lluvia se define como:

```text
precipitación > 1 mm
```

Es una definición propia del proyecto y se puede ajustar más adelante.

---

# Variables climáticas

La siguiente capa convierte las medidas climáticas en bruto en variables que después podrá usar el motor de recomendación.

Las variables actuales son:

### Temperatura

`pleasant_temperature`

Indica si la temperatura media histórica está entre 18 °C y 28 °C.

`temperature_distance`

Distancia absoluta a 25 °C.

`temperature_score`

Puntuación de 0 a 100 según la distancia a 25 °C.

La escala actual toma ±10 °C respecto a 25 °C como los límites de la puntuación.

---

### Lluvia

`rain_score`

Puntuación de 0 a 100 según la precipitación mensual histórica.

La escala del MVP es:

```text
0 mm      → 100
300+ mm   → 0
```

con una transición lineal entre ambos extremos.

Es una primera versión deliberadamente simple y fácil de explicar; no pretende decir que 300 mm sea un umbral universal de buen tiempo.

---

### Sol

`sunshine_score`

Puntuación de 0 a 100 según las horas de sol diarias promedio.

La escala actual es:

```text
0 horas    → 0
12+ horas  → 100
```

---

### Viento

`wind_score`

Puntuación de 0 a 100 según el promedio mensual de la velocidad máxima diaria del viento.

La escala actual es:

```text
10 km/h    → 100
30+ km/h   → 0
```

con una transición lineal.

Una limitación importante: esta variable es el **promedio de las máximas diarias**, no el viento que se nota de media a lo largo del día.

---

## Dataset de variables actual

El resultado está en:

```text
data/processed/climate_features.csv
```

Tamaño actual:

```text
120 filas × 16 columnas
```

Las comprobaciones de calidad confirman que:

* No hay valores nulos
* Hay 12 meses por destino
* No hay combinaciones `destination_id + month` duplicadas

---

# Principios de diseño

Hay algunas ideas que guían el proyecto desde el principio.

### Explicabilidad antes que cajas negras

El sistema debería poder explicar por qué recomienda un destino.

Por ejemplo:

```text
Clima         91
Playa         97
Ciudad        82
Precio        74
Vuelos        79
Actividades   88
```

en lugar de devolver solo:

```text
Puntuación final: 86,4
```

Cualquier recomendación tiene que poder rastrearse hasta los datos de los que sale.

---

### Variables y preferencias van por separado

El proyecto separa a propósito:

```text
Datos en bruto
    ↓
Variables
    ↓
Preferencias del usuario
    ↓
Recomendación
```

Por ejemplo, 25 °C se puede representar como una variable climática sin importar si a un viajero le gusta el calor o prefiere temperaturas suaves.

Así, usuarios distintos podrán obtener recomendaciones distintas a partir de los mismos datos de destino.

---

### Reproducibilidad

Siempre que sea posible, los datos se obtendrán de APIs o datasets documentados, sin introducir valores a mano.

De cada fuente externa se documentará:

* Fuente
* Endpoint / dataset
* Variables utilizadas
* Frecuencia de actualización
* Limitaciones
* Licencia
* Transformación aplicada

---

# Hoja de ruta

## 1. Datos de clima

* [x] Dataset semilla de destinos
* [x] Ingesta de previsión de Open-Meteo
* [x] Ingesta de clima histórico
* [x] Transformación del clima diario
* [x] Agregación de clima mensual
* [x] Cálculo de días de lluvia
* [x] Ingeniería de variables climáticas
* [x] Comprobaciones de calidad de datos

## 2. Inteligencia de destinos

* [ ] Ingesta de OpenStreetMap / Overpass
* [ ] Recuento de atracciones turísticas
* [ ] Datos de playas
* [ ] Puntos de interés de naturaleza
* [ ] Museos y atracciones culturales
* [ ] Indicadores de restaurantes / vida nocturna
* [ ] Variables a nivel de destino

## 3. Motor de recomendación

* [ ] Definir restricciones estrictas
* [ ] Definir preferencias del usuario
* [ ] Puntuación de clima
* [ ] Puntuación de destinos
* [ ] Desglose explicable de la recomendación
* [ ] Comparación de destinos

## 4. Costes del viaje

* [ ] Datos de vuelos
* [ ] Datos de alojamiento
* [ ] Estimación de gasto diario
* [ ] Estimación del coste total del viaje
* [ ] Restricciones de presupuesto

## 5. Aplicación

* [ ] Backend con FastAPI
* [ ] Endpoint de recomendación de destinos
* [ ] Interfaz web
* [ ] Comparación de destinos
* [ ] Visualizaciones de clima
* [ ] Constructor de viajes
* [ ] Mapas

## 6. Mejoras futuras

* [ ] Catálogo de destinos más grande
* [ ] Viajes con varios destinos
* [ ] Optimización de rutas
* [ ] Experimentos de machine learning
* [ ] Evaluación de las recomendaciones

---

# Stack técnico

Actual:

* Python
* pandas
* httpx
* DuckDB
* PyArrow
* Jupyter
* CSV / Parquet

Previsto:

* FastAPI
* PostgreSQL
* Next.js / TypeScript
* Tailwind CSS
* Leaflet o Mapbox
* Docker

La idea es que el proyecto siga siendo **gratuito de ejecutar durante el desarrollo**, usando APIs gratuitas, datasets abiertos y herramientas locales siempre que se pueda.

---

# ¿Por qué este proyecto?

No se trata de hacer otra web de viajes más.

Lo interesante es el problema de datos que hay detrás:

* fuentes de datos diferentes
* granularidades distintas
* información histórica frente a información actual
* datos que faltan
* consultas geográficas
* ingeniería de variables
* preferencias del usuario
* recomendaciones explicables

La aplicación final es solo la parte visible de un pipeline de datos mucho más grande.

---

## Primer hito

> Dado un destino y un mes, construir un perfil climático fiable que se pueda comparar con el de otros destinos.

Cuando esa base esté sólida, el proyecto podrá crecer hasta convertirse en el sistema completo de recomendación de viajes.


### Atribución

Los datos meteorológicos proceden de [Open-Meteo.com](https://open-meteo.com/) y se
distribuyen bajo licencia [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Los datos diarios originales se han agregado a nivel mensual y se han usado para
calcular variables derivadas (puntuaciones de temperatura, lluvia, sol y viento).