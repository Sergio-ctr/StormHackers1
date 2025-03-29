import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import DBSCAN
from geopy.distance import great_circle


# --- 1. Cargar datos básicos --- con facultades de la UAQ : Juriquilla, Jalpan, Aeropuerto, y corregidora
data = {
    'lat': [20.70472036333144, 20.584635606660438, 20.624500104570632, 20.557863075627232, 21.21693796114088, 19.4350],
    'lon': [-100.4434166888255, -100.41203832720865,  -100.36870001951225, -100.42062873485645, -99.46049430966147, -99.1300],
    'timestamp': [
        '2023-10-01 08:00:00', '2023-10-01 08:05:00',
        '2023-10-01 08:10:00', '2023-10-01 08:15:00',
        '2023-10-01 08:20:00', '2023-10-01 08:25:00'
    ],
    'velocidad': [0, 30, 40, 50, 45, 0]  # en km/h
}

df = pd.DataFrame(data)
df['timestamp'] = pd.to_datetime(df['timestamp'])

# --- 2. Análisis Exploratorio ---
print("\n--- Resumen de Datos ---")
print(df.describe())

# Visualización de la ruta
plt.figure(figsize=(10, 6))
sns.scatterplot(x='lon', y='lat', data=df, hue='velocidad', palette='viridis', size='velocidad')
plt.title('Ruta de Movimiento (Color: Velocidad)')
plt.xlabel('Longitud')
plt.ylabel('Latitud')
plt.grid()
plt.show()

# --- 3. Detección de Paradas ---
df['parada'] = df['velocidad'].apply(lambda x: 1 if x == 0 else 0)
print("\n--- Puntos de Parada ---")
print(df[df['parada'] == 1][['lat', 'lon', 'timestamp']])

# --- 4. Clustering para Identificar Zonas Frecuentes (DBSCAN) ---
coords = df[['lat', 'lon']].values
kms_per_radian = 6371.0088
epsilon = 0.1 / kms_per_radian  # 100 metros de radio
db = DBSCAN(eps=epsilon, min_samples=2, algorithm='ball_tree', metric='haversine').fit(coords)
df['cluster'] = db.labels_  # Corregido: 'labels_' en lugar de 'labels'

# Visualización de clusters
plt.figure(figsize=(10, 6))
sns.scatterplot(x='lon', y='lat', data=df, hue='cluster', palette='tab10')
plt.title('Clusters de Zonas Frecuentadas')
plt.xlabel('Longitud')
plt.ylabel('Latitud')
plt.grid()
plt.show()

# --- 5. Cálculo de Distancia y Tiempo entre Puntos ---
df['distancia_km'] = 0.0
df['tiempo_min'] = 0.0

for i in range(1, len(df)):
    punto_anterior = (df.iloc[i-1]['lat'], df.iloc[i-1]['lon'])
    punto_actual = (df.iloc[i]['lat'], df.iloc[i]['lon'])
    distancia = great_circle(punto_anterior, punto_actual).km
    tiempo = (df.iloc[i]['timestamp'] - df.iloc[i-1]['timestamp']).total_seconds() / 60
    df.at[i, 'distancia_km'] = distancia
    df.at[i, 'tiempo_min'] = tiempo

print("\n--- Distancias y Tiempos entre Puntos ---")
print(df[['timestamp', 'distancia_km', 'tiempo_min', 'velocidad']])

# --- 6. Patrones de Velocidad ---
plt.figure(figsize=(10, 4))
plt.plot(df['timestamp'], df['velocidad'], marker='o')
plt.title('Patrón de Velocidad a lo Largo del Tiempo')
plt.xlabel('Tiempo')
plt.ylabel('Velocidad (km/h)')
plt.grid()
plt.show()

# --- 7. Exportar Resultados ---
df.to_csv('analisis_movimiento.csv', index=False)
print("\n¡Análisis completado! Resultados guardados en 'analisis_movimiento.csv'")