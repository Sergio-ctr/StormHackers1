import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

# Configuración de estilo
plt.style.use('ggplot')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.titlepad'] = 20

# Datos de la tabla (simplificados para el ejemplo)
data = {
    'Entidad': ['Nacional', 'Jalisco', 'EdoMex', 'EdoMex', 'EdoMex', 'Puebla', 'Jalisco',
                'Jalisco', 'Baja California', 'Queretaro', 'Sinaloa', 'San Luis Potosí',
                'EdoMex', 'EdoMex', 'Morelia', 'CdMex'],
    'Municipio': ['Nacional', 'Guadalajara', 'Ecatepec', 'Naucalpan', 'Tlalnepantla',
                  'Puebla', 'Zapopan', 'Tlaquepaque', 'Tijuana', 'Queretaro', 'Culiacan',
                  'San Luis Potosí', 'Toluca', 'Cuautitlan', 'Cuernavaca', 'Iztapalapa'],
    '2020-21': [58902, 4810, 3889, 1621, 1720, 1151, 1937, 873, 855, 856, 1447, 704, 847, 1081, 619, 857],
    '2021-22': [58406, 4345, 2974, 1538, 1742, 1230, 1809, 1061, 963, 971, 1374, 944, 1004, 1067, 599, 624],
    '2022-23': [60895, 3794, 2031, 1598, 1796, 1565, 1743, 1150, 975, 1173, 1451, 1041, 837, 726, 768, 740],
    '2023-24': [61727, 2998, 1974, 1712, 1701, 1653, 1431, 1082, 1055, 1035, 1022, 972, 946, 939, 927, 805],
    'Porcentaje': [1.4, -21.0, -2.8, 7.1, -5.3, 5.6, -17.9, -5.9, 8.2, -11.8, -29.6, -6.6, 13.0, 29.3, 20.7, 8.8]
}

df = pd.DataFrame(data)

# ---- GRÁFICA 1: Evolución nacional vs principales ciudades ----
plt.figure(figsize=(14, 8))
years = ['2020-21', '2021-22', '2022-23', '2023-24']

# Seleccionar las 5 ciudades con más robos en 2023-24
top5 = df[df['Municipio'] != 'Nacional'].nlargest(5, '2023-24')

plt.plot(years, df[df['Municipio'] == 'Nacional'].values[0][2:6],
         label='Nacional', linewidth=3, marker='o', markersize=8)

for i, row in top5.iterrows():
    plt.plot(years, row[2:6], label=f"{row['Municipio']} ({row['Entidad']})",
             linestyle='--', marker='s')

plt.title('EVOLUCIÓN DE VEHÍCULOS ROBADOS (2020-2024)', fontsize=16)
plt.ylabel('Número de vehículos robados', fontsize=12)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, linestyle='--', alpha=0.7)
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'))
plt.tight_layout()
plt.savefig('evolucion_robos.png', dpi=300, bbox_inches='tight')
plt.show()

# ---- GRÁFICA 2: Top 10 municipios 2023-24 ----
top10 = df[df['Municipio'] != 'Nacional'].nlargest(10, '2023-24')

plt.figure(figsize=(12, 6))
bars = plt.barh(top10['Municipio'] + ' (' + top10['Entidad'] + ')',
                top10['2023-24'],
                color=plt.cm.tab20(np.arange(len(top10))))

plt.title('TOP 10 MUNICIPIOS CON MÁS VEHÍCULOS ROBADOS (2023-2024)', fontsize=16)
plt.xlabel('Número de vehículos robados', fontsize=12)
plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'))

# Añadir etiquetas con porcentaje de cambio
for i, bar in enumerate(bars):
    width = bar.get_width()
    cambio = top10.iloc[i]['Porcentaje']
    color = 'red' if cambio < 0 else 'green'
    plt.text(width + 50, bar.get_y() + bar.get_height()/2,
             f'{cambio}%',
             ha='left', va='center', color=color, fontweight='bold')

plt.tight_layout()
plt.savefig('top10_municipios.png', dpi=300)
plt.show()

# ---- GRÁFICA 3: Mapa de calor de cambios porcentuales ----
pivot_df = df[df['Municipio'] != 'Nacional'].pivot_table(
    index='Entidad', columns='Municipio', values='Porcentaje'
)

plt.figure(figsize=(12, 6))
plt.imshow(pivot_df.fillna(0), cmap='RdYlGn', aspect='auto', vmin=-30, vmax=30)
plt.colorbar(label='Cambio porcentual (%)')
plt.title('CAMBIO PORCENTUAL EN VEHÍCULOS ROBADOS (2020-21 a 2023-24)', fontsize=16)
plt.xticks(np.arange(len(pivot_df.columns)), pivot_df.columns, rotation=45, ha='right')
plt.yticks(np.arange(len(pivot_df.index)), pivot_df.index)
plt.tight_layout()
plt.savefig('mapa_calor_cambios.png', dpi=300)
plt.show()