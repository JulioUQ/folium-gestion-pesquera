#  Mapas Interactivos con Folium para Gestión Pesquera

Este repositorio tiene como objetivo **aprender, comprender y aplicar** la librería [Folium](https://python-visualization.github.io/folium/) para la creación de **mapas interactivos y animados** enfocados en la gestión pesquera.

Se desarrollan ejemplos prácticos basados en datos reales o simulados, incluyendo:
- Visualización de rectángulos estadísticos.
- Mapas dinámicos y animados de la trayectoria de los buques.
- Representación de capturas y esfuerzo pesquero.
- Mapas temáticos por especie, temporada o zona.

##  Estructura del repositorio

```
folium-gestion-pesquera/  
│  
├── README.md # Explicación general del proyecto  
├── requirements.txt # Librerías necesarias  
├── data/ # Datos de ejemplo (GeoJSON, CSV, shapefiles)  
├── notebooks/ # Jupyter Notebooks con ejemplos prácticos  
│ ├── 01_basicos_folium.ipynb  
│ ├── 02_capas_geojson.ipynb  
│ ├── 03_visualizacion_especies.ipynb  
│ └── 04_interactividad_filtros.ipynb  
├── scripts/ # Scripts Python reutilizables  
│ └── folium_utils.py   
└── img/ # Capturas de ejemplo para el README
````

##  Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/usuario/folium-gestion-pesquera.git
cd folium-gestion-pesquera
````

2. **Crear un entorno virtual (opcional pero recomendado)**
```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

## Contenido de aprendizaje

|Notebook|Tema|Descripción|
|---|---|---|
|01_basicos_folium.ipynb|Mapa base|Creación de mapas, tiles y centrado|
|02_capas_y_controles_folium.ipynb|Capas vectoriales|Añadir polígonos y colorearlos según datos|
|03_visualizacion_especies.ipynb|Mapas temáticos|Colorear por especie, biomasa o esfuerzo|
|04_interactividad_filtros.ipynb|Filtros y controles|Añadir `LayerControl`, popups y leyendas|

## Tecnologías y librerías utilizadas

- [Folium](https://python-visualization.github.io/folium/)
- [GeoPandas](https://geopandas.org/)
- [Pandas](https://pandas.pydata.org/)
- [Shapely](https://shapely.readthedocs.io/)
- [Jupyter Notebook](https://jupyter.org/)

