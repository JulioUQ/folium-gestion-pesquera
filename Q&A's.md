# **¿Cuando usar add_child() o add_to()?**

La diferencia entre `add_child()` y `add_to()` en Folium es más de **estilo y orden de escritura** que de funcionalidad, pero hay matices que merece la pena entender.


##  **add\_child()**

* **Forma clásica** usada internamente en Folium.
* Llamas al método **sobre el mapa o sobre otro objeto contenedor** y le pasas el elemento que quieres añadir como argumento.
* **Orden:**

  1. Creas el elemento.
  2. Lo pasas a `add_child()` del mapa (o capa padre).

**Ejemplo:**

```python
m = folium.Map(location=[40.4168, -3.7038], zoom_start=13)

marker = folium.Marker(location=[40.4183, -3.7028], popup="Puerta del Sol")
m.add_child(marker)  # Añadido al mapa
```

## **add\_to()**

* **Forma encadenada** más moderna y habitual en ejemplos recientes.
* Llamas al método **sobre el elemento** y le pasas el mapa o capa donde quieres añadirlo.
* Permite escribir código más compacto.
* Útil para **encadenar varias operaciones** de forma fluida.

**Ejemplo:**

```python
m = folium.Map(location=[40.4168, -3.7038], zoom_start=13)

folium.Marker(location=[40.4183, -3.7028], popup="Puerta del Sol").add_to(m)
```

##  **Comparativa**

| Aspecto                   | `add_child()`                     | `add_to()`                       |
| ------------------------- | --------------------------------- | -------------------------------- |
| **Punto de llamada**      | En el mapa o contenedor           | En el elemento                   |
| **Estilo**                | Más explícito (padre → hijo)      | Más fluido (hijo → padre)        |
| **Encadenamiento**        | Menos práctico                    | Permite encadenar                |
| **Uso interno en Folium** | Muy común                         | Más para usuarios                |
| **Legibilidad**           | Mejor si hay jerarquías complejas | Mejor para código rápido y claro |

**Regla práctica**:

* Si estás construyendo **objetos por separado** y luego quieres añadirlos, `add_child()` es más claro.
* Si creas y añades **en la misma línea**, `add_to()` es más limpio.


---


# **¿Cuando usar folium.CircleMarker o folium.Marker?**

La diferencia entre `folium.CircleMarker` y `folium.Marker` está en **el tipo de elemento que representan y cómo se visualizan en el mapa**.

## **folium.Marker**

* **Función:** Coloca un icono en una posición específica del mapa.
* **Visualización:** Usa un **icono (por defecto azul con símbolo de ubicación)**, pero puede personalizarse con `folium.Icon`.
* **Escala:** El icono **no cambia de tamaño con el zoom** (tamaño fijo en píxeles).
* **Interactividad:** Puede tener `popup`, `tooltip` y un icono personalizado.
* **Uso típico:** Marcar lugares de interés con un símbolo reconocible.

**Ejemplo:**

```python
folium.Marker(
    location=[40.4168, -3.7038],
    popup="Ubicación",
    tooltip="Clic para más info",
    icon=folium.Icon(color="red", icon="info-sign")
).add_to(m)
```

## **folium.CircleMarker**

* **Función:** Dibuja un **círculo plano** sobre el mapa en una posición específica.
* **Visualización:** Un círculo vectorial renderizado en el mapa.
* **Escala:** **No cambia de tamaño en metros**, el tamaño es fijo en píxeles (ej. `radius=10`), así que al hacer zoom el círculo se ve más grande o más pequeño en proporción al mapa.
* **Personalización:** Control total sobre color de borde (`color`), color de relleno (`fill_color`), opacidad (`fill_opacity`), etc.
* **Uso típico:** Representar datos cuantitativos o visualizaciones densas (por ejemplo, puntos en un mapa de calor manual).

**Ejemplo:**

```python
folium.CircleMarker(
    location=[40.4168, -3.7038],
    radius=8,
    color="blue",
    fill=True,
    fill_color="blue",
    fill_opacity=0.6,
    popup="Círculo marcador"
).add_to(m)
```

## **Comparativa**

| Característica  | `folium.Marker`         | `folium.CircleMarker`           |
| --------------- | ----------------------- | ------------------------------- |
| Representación  | Icono gráfico           | Círculo vectorial               |
| Tamaño          | Fijo en píxeles         | Radio fijo en píxeles           |
| Personalización | Iconos de `folium.Icon` | Colores y opacidad del círculo  |
| Ideal para      | Puntos de interés       | Representar magnitud o densidad |

**Regla práctica:**

* Si quieres un **símbolo reconocible** (hotel, restaurante, monumento) → `folium.Marker`.
* Si quieres un **círculo proporcional a un dato o simple punto visual** → `folium.CircleMarker`.