
# ================================
# geo_functions.py
# Funciones para análisis de geodatos
# ================================

import sys
import os
import warnings
import pandas as pd
from pandas._typing import MergeHow
import geopandas as gpd
from shapely import wkt  
from shapely.geometry import Point, Polygon, MultiPolygon, LineString

# Añadir directorio raíz al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
warnings.simplefilter(action='ignore', category=UserWarning)

# ====================================
# FUNCIONES DE GEOPANDAS / ESPACIALES
# ====================================

def import_shp_as_gpd(shapefile: str) -> gpd.GeoDataFrame:
    """Importa shapefile como GeoDataFrame con CRS EPSG:4326.

    Ejemplo:
        gdf = import_shp_as_gpd("/ruta/archivo.shp")
    """
    gdf = gpd.read_file(shapefile)
    return gdf.to_crs(epsg=4326) if gdf.crs else gdf.set_crs(epsg=4326)

from shapely import wkt  # Necesario para convertir WKT a geometría

def pd_to_gpd(df: pd.DataFrame, longitud_col: str = "longitude", latitud_col: str = "latitude") -> gpd.GeoDataFrame:
    """Convierte un DataFrame a GeoDataFrame usando columnas de latitud/longitud o geometría en WKT."""

    df = df.copy()

    if longitud_col in df.columns and latitud_col in df.columns:
        geometry = [Point(xy) for xy in zip(df[longitud_col], df[latitud_col])]
        return gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')

    if "geometry" in df.columns and df["geometry"].dtype == "object":
        try:
            df["geometry"] = gpd.GeoSeries.from_wkt(df["geometry"])
            return gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")
        except Exception as e:
            raise ValueError(f"No se pudo convertir la columna 'geometry' desde WKT: {e}")

    raise ValueError("No se encontraron columnas de latitud/longitud ni geometría en WKT.")


def drop_z(geom):
    """Convertir geometrías a 2D eliminando coordenada Z

    Ejemplo:
        gdf["geometry"] = gdf["geometry"].apply(drop_z)
    """
    if geom is None:
        return None
    if isinstance(geom, Polygon):
        return Polygon(
            [(x, y) for x, y, *_ in geom.exterior.coords],
            [ [(x, y) for x, y, *_ in ring.coords] for ring in geom.interiors ]
        )
    elif isinstance(geom, MultiPolygon):
        return MultiPolygon([drop_z(p) for p in geom.geoms])
    return geom


def generar_trayectoria(df, lat_col="Latitud", lon_col="Longitud", fecha_col="FcIval"):
    """
    Genera una geometría de línea representando la trayectoria de un buque
    ordenada de menor a mayor fecha y devuelve el tiempo de ruta.
    Funciona tanto si df tiene una columna 'geometry' como si se proporcionan lat/lon.

    Parámetros:
        df (DataFrame o GeoDataFrame): Datos de posiciones del buque.
        lat_col (str): Nombre de la columna de latitud si no hay geometría.
        lon_col (str): Nombre de la columna de longitud si no hay geometría.
        fecha_col (str): Nombre de la columna de fecha/hora.

    Retorna:
        GeoDataFrame con una única geometría LineString y tiempo total de ruta (en horas).
    """
    # Ordenar por fecha
    df_sorted = df.sort_values(fecha_col)

    # Determinar coordenadas
    if "geometry" in df_sorted.columns:
        coords = [(geom.x, geom.y) for geom in df_sorted.geometry]
    else:
        coords = list(zip(df_sorted[lon_col], df_sorted[lat_col]))

    # Crear LineString
    linea = LineString(coords)

    # Calcular tiempo total de ruta
    tiempo_total = (pd.to_datetime(df_sorted[fecha_col].iloc[-1]) -
                    pd.to_datetime(df_sorted[fecha_col].iloc[0])).total_seconds() / 3600  # horas

    # Crear GeoDataFrame
    gdf_trayectoria = gpd.GeoDataFrame(
        {"tiempo_horas": [tiempo_total]},
        geometry=[linea],
        crs="EPSG:4326"
    )

    return gdf_trayectoria


def exportar_gdf_shapefile(gdf: gpd.GeoDataFrame, path_out: str, overwrite: bool = True) -> None:
    """Exporta un GeoDataFrame a shapefile en EPSG:4326.

    Ejemplo:
        exportar_gdf_shapefile(gdf, "./salida.shp")
    """
    if gdf.empty:
        raise ValueError("GeoDataFrame vacío.")
    if not gdf.geometry.is_valid.all():
        raise ValueError("Geometrías inválidas.")

    path_out = os.path.abspath(path_out)
    if os.path.exists(path_out) and not overwrite:
        raise FileExistsError(f"'{path_out}' ya existe y overwrite=False.")

    gdf.to_crs(epsg=4326).to_file(path_out, driver='ESRI Shapefile', encoding='utf-8')