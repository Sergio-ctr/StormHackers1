import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter

# Configuración de estilo (usando un estilo disponible)
plt.style.use('ggplot')  # Cambiado a 'ggplot' que es un estilo similar y disponible
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.titlepad'] = 20

# Crear DataFrame con los datos
data = {
    'Entidad': ['Aguascalientes', 'Baja California', 'Baja California Sur', 'Campeche',
                'Coahuila', 'Colima', 'Chiapas', 'Chihuahua', 'CDMX', 'Durango',
                'Guanajuato', 'Guerrero', 'Hidalgo', 'Jalisco', 'México', 'Michoacán',
                'Morelos', 'Nayarit', 'Nuevo León', 'Oaxaca', 'Puebla', 'Querétaro',
                'Quintana Roo', 'San Luis Potosí', 'Sinaloa', 'Sonora', 'Tabasco',
                'Tamaulipas', 'Tlaxcala', 'Veracruz', 'Yucatán', 'Zacatecas'],
    'Total_Eventos': [4473, 11782, 6045, 4574, 10876, 6225, 4065, 26559, 7276, 11631,
                      17703, 7414, 4593, 14293, 21105, 16196, 8864, 2852, 80582, 5203,
                      13423, 9307, 6619, 6775, 7230, 26557, 2492, 14090, 1674, 9659,
                      8478, 2433],
    'Colision_Vehiculo': [1955, 8120, 4246, 2204, 7345, 3365, 2268, 19606, 4262, 6900,
                          7550, 3954, 2666, 7444, 12770, 8039, 3733, 1091, 58617, 2130,
                          9152, 4761, 2776, 4037, 3224, 19326, 1041, 9641, 932, 5987,
                          2343, 1024],
    'Colision_Peaton': [154, 592, 116, 75, 300, 94, 120, 1055, 793, 314,
                        579, 277, 115, 320, 874, 506, 319, 99, 1874, 165,
                        462, 229, 245, 162, 320, 686, 51, 301, 81, 274,
                        232, 69]
}

df = pd.DataFrame(data)

# ---- GRÁFICA 1: Top 10 estados con más accidentes ----
top10 = df.nlargest(10, 'Total_Eventos')

fig, ax = plt.subplots(figsize=(14, 8))
x = np.arange(len(top10['Entidad']))
width = 0.25

rects1 = ax.bar(x - width, top10['Total_Eventos'], width, label='Total Eventos', color='#1f77b4')
rects2 = ax.bar(x, top10['Colision_Vehiculo'], width, label='Colisión con vehículo', color='#ff7f0e')
rects3 = ax.bar(x + width, top10['Colision_Peaton'], width, label='Colisión con peatón', color='#2ca02c')

ax.set_title('TOP 10 ESTADOS CON MÁS ACCIDENTES VIALES (2023)', fontsize=16)
ax.set_xticks(x)
ax.set_xticklabels(top10['Entidad'], rotation=45, ha='right')
ax.legend()
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'))

# Añadir etiquetas
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:,}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

plt.tight_layout()
plt.savefig('top10_accidentes.png', dpi=300)
plt.show()

# ---- GRÁFICA 2: Proporción de tipos de accidente ----
df['Otros'] = df['Total_Eventos'] - df['Colision_Vehiculo'] - df['Colision_Peaton']
accident_types = df[['Colision_Vehiculo', 'Colision_Peaton', 'Otros']].sum()
labels = ['Colisión con vehículo', 'Colisión con peatón', 'Otros accidentes']

fig, ax = plt.subplots(figsize=(10, 8))
wedges, texts, autotexts = ax.pie(accident_types,
                                  labels=labels,
                                  autopct='%1.1f%%',
                                  startangle=90,
                                  colors=['#ff7f0e', '#2ca02c', '#d62728'],
                                  textprops={'fontsize': 12})

ax.set_title('DISTRIBUCIÓN NACIONAL DE TIPOS DE ACCIDENTE (2023)', fontsize=16)
plt.savefig('distribucion_accidentes.png', dpi=300)
plt.show()

# ---- GRÁFICA 3: Comparativo Querétaro vs Promedio Nacional ----
queretaro = df[df['Entidad'] == 'Querétaro'].iloc[0]
nacional_avg = df[['Colision_Vehiculo', 'Colision_Peaton']].mean()

fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(2)
width = 0.35

rects1 = ax.bar(x - width/2, [queretaro['Colision_Vehiculo'], queretaro['Colision_Peaton']],
                width, label='Querétaro', color='#9467bd')
rects2 = ax.bar(x + width/2, [nacional_avg['Colision_Vehiculo'], nacional_avg['Colision_Peaton']],
                width, label='Promedio Nacional', color='#8c564b')

ax.set_title('COMPARATIVO QUERÉTARO VS PROMEDIO NACIONAL', fontsize=16)
ax.set_xticks(x)
ax.set_xticklabels(['Colisión con vehículo', 'Colisión con peatón'])
ax.legend()
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'))

autolabel(rects1)
autolabel(rects2)

plt.tight_layout()
plt.savefig('queretaro_vs_nacional.png', dpi=300)
plt.show()