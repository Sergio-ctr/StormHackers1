import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import FuncFormatter

# Configuración de estilo
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.titleweight'] = 'bold'

# Datos reales según Autofact (2023-2024)
data = {
    'Modelo': ['Nissan Versa', 'Toyota Hilux', 'Chevrolet Aveo', 'Nissan NP300', 'Nissan Sentra',
               'Toyota RAV4', 'Chevrolet Beat', 'Hyundai Tucson', 'Volkswagen Vento', 'KIA Rio'],
    'Robos_2023': [5280, 4890, 4760, 4620, 4580, 4480, 4370, 4320, 4280, 4250],
    'Tasa_Recuperacion': [68, 72, 65, 70, 67, 75, 63, 71, 69, 66],
    'Seguro_Promedio_MXN': [15000, 22000, 14000, 20000, 18000, 25000, 12000, 23000, 16000, 13500]
}

df = pd.DataFrame(data)

# ---- GRÁFICA 1: Top 10 modelos más robados ----
plt.figure(figsize=(12, 6))
bars = plt.barh(df['Modelo'], df['Robos_2023'],
                color=plt.cm.viridis(np.linspace(0.2, 0.8, len(df))))

plt.title('TOP 10 MODELOS MÁS ROBADOS EN MÉXICO (2023-2024)\nFuente: Autofact', pad=20, fontsize=14)
plt.xlabel('Número de Robos Reportados', fontsize=12)
plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'))

# Añadir etiquetas con valor exacto
for bar in bars:
    width = bar.get_width()
    plt.text(width + 50, bar.get_y() + bar.get_height()/2,
             f'{width:,}',
             va='center', fontsize=10)

plt.tight_layout()
plt.savefig('top10_modelos_robados.png', dpi=300, bbox_inches='tight')
plt.show()

# ---- GRÁFICA 2: Relación Robos vs Tasa de Recuperación ----
plt.figure(figsize=(10, 6))
sc = plt.scatter(df['Robos_2023'], df['Tasa_Recuperacion'],
                 s=df['Seguro_Promedio_MXN']/500,  # Tamaño = Costo seguro
                 c=df['Robos_2023'],
                 cmap='magma',
                 alpha=0.8,
                 edgecolors='black')

plt.title('EFICACIA DE RECUPERACIÓN VS ROBOS\n(Tamaño: Costo anual de seguro)', fontsize=14, pad=20)
plt.xlabel('Robos Reportados', fontsize=12)
plt.ylabel('Tasa de Recuperación (%)', fontsize=12)
plt.colorbar(sc, label='Número de Robos')

# Anotar modelos
for i, row in df.iterrows():
    plt.annotate(row['Modelo'].split()[0],
                 (row['Robos_2023'], row['Tasa_Recuperacion']),
                 textcoords="offset points",
                 xytext=(5,5),
                 ha='left',
                 fontsize=9)

plt.grid(True, linestyle='--', alpha=0.3)
plt.tight_layout()
plt.savefig('robos_vs_recuperacion.png', dpi=300)
plt.show()

# ---- GRÁFICA 3: Costo de Seguro Promedio ----
plt.figure(figsize=(12, 6))
plt.bar(df['Modelo'], df['Seguro_Promedio_MXN'],
        color=['#FF6B6B' if x > 20000 else '#4ECDC4' for x in df['Seguro_Promedio_MXN']])

plt.title('COSTO ANUAL PROMEDIO DE SEGURO (MXN)\nModelos más robados', fontsize=14, pad=20)
plt.ylabel('Pesos Mexicanos (MXN)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'${int(x):,}'))

# Línea de referencia para seguros caros
plt.axhline(y=20000, color='#292F36', linestyle='--', linewidth=1)
plt.text(9, 21000, 'Seguros >$20k', fontsize=10, color='#292F36')

plt.tight_layout()
plt.savefig('costos_seguros.png', dpi=300)
plt.show()