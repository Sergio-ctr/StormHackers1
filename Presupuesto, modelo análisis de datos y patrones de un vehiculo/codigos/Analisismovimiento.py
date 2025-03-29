import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import DBSCAN
from geopy.distance import great_circle


class AnalizadorMovimientos:
    def __init__(self, datos):
        self.df = pd.DataFrame(datos)
        self._preprocesar()

    def _preprocesar(self):
        """Prepara los datos iniciales"""
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        self.df['parada'] = self.df['velocidad'].apply(lambda x: 1 if x == 0 else 0)

    def analizar(self):
        """Ejecuta todo el análisis"""
        self._analisis_exploratorio()
        self._detectar_paradas()
        self._clusterizar()
        self._calcular_distancias()
        self._graficar_velocidad()
        self._exportar()

    def _analisis_exploratorio(self):
        """Muestra estadísticas básicas y gráfico inicial"""
        print("\n--- Resumen de Datos ---")
        print(self.df.describe())

        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='lon', y='lat', data=self.df,
                        hue='velocidad', palette='viridis', size='velocidad')
        plt.title('Ruta de Movimiento (Color: Velocidad)')
        plt.xlabel('Longitud')
        plt.ylabel('Latitud')
        plt.grid()
        plt.show()

    def _detectar_paradas(self):
        """Identifica puntos de parada"""
        print("\n--- Puntos de Parada ---")
        print(self.df[self.df['parada'] == 1][['lat', 'lon', 'timestamp']])

    def _clusterizar(self):
        """Agrupa ubicaciones frecuentes"""
        coords = self.df[['lat', 'lon']].values
        kms_por_radian = 6371.0088
        epsilon = 0.1 / kms_por_radian

        db = DBSCAN(eps=epsilon, min_samples=2,
                    algorithm='ball_tree', metric='haversine').fit(coords)
        self.df['cluster'] = db.labels_

        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='lon', y='lat', data=self.df,
                        hue='cluster', palette='tab10')
        plt.title('Zonas Frecuentadas (Clusters)')
        plt.xlabel('Longitud')
        plt.ylabel('Latitud')
        plt.grid()
        plt.show()

    def _calcular_distancias(self):
        """Calcula distancias y tiempos entre puntos"""
        self.df['distancia_km'] = 0.0
        self.df['tiempo_min'] = 0.0

        for i in range(1, len(self.df)):
            punto_anterior = (self.df.iloc[i - 1]['lat'], self.df.iloc[i - 1]['lon'])
            punto_actual = (self.df.iloc[i]['lat'], self.df.iloc[i]['lon'])

            self.df.at[i, 'distancia_km'] = great_circle(punto_anterior, punto_actual).km
            self.df.at[i, 'tiempo_min'] = (self.df.iloc[i]['timestamp'] -
                                           self.df.iloc[i - 1]['timestamp']).total_seconds() / 60

        print("\n--- Distancias y Tiempos ---")
        print(self.df[['timestamp', 'distancia_km', 'tiempo_min', 'velocidad']])

    def _graficar_velocidad(self):
        """Muestra patrón de velocidad"""
        plt.figure(figsize=(10, 4))
        plt.plot(self.df['timestamp'], self.df['velocidad'], marker='o')
        plt.title('Patrón de Velocidad')
        plt.xlabel('Tiempo')
        plt.ylabel('Velocidad (km/h)')
        plt.grid()
        plt.show()

    def _exportar(self):
        """Guarda resultados"""
        self.df.to_csv('analisis_movimiento.csv', index=False)
        print("\n¡Análisis completado! Resultados en 'analisis_movimiento.csv'")


# Coordenadas de las facultades UAQ: Juriquilla, Jalpan, Aeropuerto, y corregidora
datos_ejemplo = {
    'lat': [20.70472036333144, 20.584635606660438, 20.624500104570632, 20.557863075627232, 21.21693796114088, 19.4350],
    'lon': [-100.4434166888255, -100.41203832720865,  -100.36870001951225, -100.42062873485645, -99.46049430966147, -99.1300],
    'timestamp': [
        '2023-10-01 08:00:00', '2023-10-01 08:05:00',
        '2023-10-01 08:10:00', '2023-10-01 08:15:00',
        '2023-10-01 08:20:00', '2023-10-01 08:25:00'
    ],
    'velocidad': [0, 30, 40, 50, 45, 0]
}

# Uso del analizador
analizador = AnalizadorMovimientos(datos_ejemplo)
analizador.analizar()