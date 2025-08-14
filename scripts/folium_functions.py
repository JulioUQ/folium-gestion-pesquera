"""
folium_functions.py
Funciones para inicializar y enriquecer mapas base en Folium de forma genérica.
"""

import folium
from folium.features import DivIcon
from shapely.geometry import MultiPolygon, Polygon
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as mcm


def centrar_mapa(gdf, zoom=9, tiles="CartoDB positron"):
    """
    Centra un mapa en el centroide de un GeoDataFrame.

    Parámetros:
        gdf (GeoDataFrame): Datos espaciales.
        zoom (int): Nivel de zoom.
        tiles (str): Estilo de mapa.

    Retorna:
        folium.Map centrado.
    """
    centro = gdf.geometry.union_all().centroid
    return folium.Map(location=[centro.y, centro.x], zoom_start=zoom, tiles=tiles)


def añadir_contornos(m, gdf, columna_grupo, color_map=None, emoji_map=None, tooltip_fields=None, tooltip_aliases=None):
    """
    Añade contornos agrupados por un valor de columna.

    Parámetros:
        m (folium.Map): Mapa base.
        gdf (GeoDataFrame): Datos espaciales.
        columna_grupo (str): Columna por la que agrupar.
        color_map (dict): Diccionario valor → color.
        emoji_map (dict): Diccionario valor → emoji.
        tooltip_fields (list): Columnas para tooltip.
        tooltip_aliases (list): Alias de las columnas para tooltip.
    """
    for valor, grupo in gdf.groupby(columna_grupo):
        color = color_map.get(valor, "#999999") if color_map else "#999999"
        emoji = emoji_map.get(valor, "") if emoji_map else ""

        folium.GeoJson(
            data=grupo,
            name=f"{emoji} {valor}" if emoji else str(valor),
            style_function=lambda x, col=color: {
                "fillColor": col,
                "color": col,
                "weight": 2,
                "fillOpacity": 0
            },
            tooltip=folium.GeoJsonTooltip(fields=tooltip_fields, aliases=tooltip_aliases) if tooltip_fields else None
        ).add_to(m)


def añadir_etiquetas_por_poligono(m, gdf, columna, color_texto="black"):
    """
    Añade etiquetas de texto en el centroide de cada polígono.

    Parámetros:
        m (folium.Map): Mapa base.
        gdf (GeoDataFrame): Datos espaciales.
        columna (str): Columna cuyo valor se mostrará como etiqueta.
        color_texto (str): Color del texto.
    """
    for _, row in gdf.iterrows():
        valor = row[columna]
        geom = row["geometry"]

        geoms = list(geom.geoms) if isinstance(geom, MultiPolygon) else [geom] if isinstance(geom, Polygon) else []
        for poly in geoms:
            centroide = poly.centroid
            folium.Marker(
                location=[centroide.y, centroide.x],
                icon=DivIcon(
                    icon_size=(100, 20),
                    icon_anchor=(0, 0),
                    html=f'<div style="font-size: 11pt; font-weight: bold; color: {color_texto}">{valor}</div>',
                )
            ).add_to(m)


def añadir_poligonos_por_valor(
    m,
    gdf,
    columna_nombre,
    tooltip_fields=None,
    tooltip_aliases=None,
    cmap_name="tab20",
    fill_opacity=0.4
):
    """
    Añade polígonos coloreados por un valor único de columna.

    Parámetros:
        m (folium.Map): Mapa base.
        gdf (GeoDataFrame): Datos espaciales.
        columna_nombre (str): Columna que define las categorías.
        tooltip_fields (list): Columnas para tooltip.
        tooltip_aliases (list): Alias para tooltip.
        cmap_name (str): Nombre del colormap de Matplotlib.
        fill_opacity (float): Opacidad del relleno.
    """
    nombres_unicos = gdf[columna_nombre].dropna().unique()
    cmap = plt.colormaps[cmap_name].resampled(len(nombres_unicos))
    colores = [cmap(i) for i in range(len(nombres_unicos))]
    color_map = {
        nombre: f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'
        for nombre, (r, g, b, _) in zip(nombres_unicos, colores)
    }

    for nombre in nombres_unicos:
        color = color_map[nombre]
        sub_gdf = gdf[gdf[columna_nombre] == nombre]

        folium.GeoJson(
            sub_gdf,
            name=f'<span style="color:{color}">{nombre}</span>',
            style_function=lambda x, col=color: {
                "fillColor": col,
                "color": "black",
                "weight": 1,
                "fillOpacity": fill_opacity
            },
            tooltip=folium.GeoJsonTooltip(fields=tooltip_fields, aliases=tooltip_aliases) if tooltip_fields else None
        ).add_to(m)


def añadir_puntos(
    m,
    gdf,
    lat_col="Latitud",
    lon_col="Longitud",
    color_col=None,
    tooltip_text=None,
    cmap_name="tab10"
):
    """
    Añade puntos al mapa, coloreados por categoría si se indica.

    Parámetros:
        m (folium.Map): Mapa base.
        gdf (GeoDataFrame o DataFrame): Datos con coordenadas.
        lat_col (str): Columna de latitud.
        lon_col (str): Columna de longitud.
        color_col (str): Columna que define el color (opcional).
        tooltip_text (str o lista): Texto o lista de columnas para tooltip.
        cmap_name (str): Nombre del colormap de Matplotlib.
    """
    if color_col:
        categorias = gdf[color_col].unique()
        colormap = mcm.get_cmap(cmap_name, len(categorias))
        color_dict = {
            cat: mcolors.rgb2hex(colormap(i))
            for i, cat in enumerate(categorias)
        }
    else:
        color_dict = {None: "blue"}

    for _, row in gdf.iterrows():
        color = color_dict[row[color_col]] if color_col else "blue"

        if isinstance(tooltip_text, list):
            tooltip_html = "<br>".join(f"{col}: {row[col]}" for col in tooltip_text)
        elif isinstance(tooltip_text, str):
            tooltip_html = tooltip_text
        else:
            tooltip_html = None

        folium.CircleMarker(
            location=[row[lat_col], row[lon_col]],
            radius=2,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            tooltip=folium.Tooltip(tooltip_html, sticky=True) if tooltip_html else None
        ).add_to(m)
