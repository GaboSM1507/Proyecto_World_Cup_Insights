# World Cup Insights - Proyecto Programación II #

En el siguiente trabajo se realiza un sistema en Python orientado a objetos que 
ingesta, procesa, analiza y visualiza los partidos de la FIFA World Cup (1930-2026), a
partir del dataset público "International football results from 1872
to 2026" (martj42, GitHub).

El proyecto está estructurado en clases con responsabilidades bien
separadas: una se encarga de descargar y guardar los datos, otra de
responder consultas sobre los partidos, otra de limpiar los datos y
calcular estadísticas, y otra de generar las visualizaciones. Además
de los scripts en Python, el proyecto incluye dos notebooks de Jupyter
con el análisis paso a paso, y un dashboard interactivo hecho con
Streamlit para explorar los resultados de forma visual.

Proyecto II - BD-143 Programación II - Colegio Universitario de Cartago.

## Estructura del proyecto ##

- **`src/`** : todo el código fuente del proyecto, organizado por responsabilidad.
  - `src/ingesta/` : clase `CargadorDatos`: descarga el CSV público, filtra los
    partidos de Copa Mundial, y guarda los resultados en `data/raw/` y
    `data/processed/`.
  - `src/gestor/` : clase `GestorPartidos`: expone consultas de solo lectura
    sobre los partidos (por equipo, por año, por sede, ventaja de local, etc.).
  - `src/eda/` : clase `ProcesadorEDA`: limpia los datos, agrega columnas
    derivadas (año, total de goles, diferencia de goles, ganador) y calcula
    estadísticas descriptivas y correlaciones.
  - `src/visualizacion/` : clase `Visualizador`: genera las 7 gráficas del
    proyecto (líneas, barras, histograma, heatmap, scatter).
  - `src/helpers/` : clase `Utilidades`: funciones auxiliares reutilizables
    (validaciones, formateo).
  - `src/main.py` : punto de entrada del proyecto; ejecuta todo el flujo en
    orden (ingesta: limpieza → persistencia → consultas → visualización).
- **`notebooks/`** : análisis en Jupyter, paso a paso.
  - `01_EDA.ipynb` : ingesta, limpieza y análisis exploratorio.
  - `02_Visualizacion.ipynb` : generación e interpretación de las gráficas.
- **`data/`** : datos del proyecto.
  - `data/raw/` : CSV filtrado (solo partidos de la FIFA World Cup), sin procesar.
  - `data/processed/` : CSV con los datos ya limpios y columnas derivadas.
- **`reports/figures/`** : las 7 gráficas generadas, en formato PNG.
- **`dashboard/app.py`** : dashboard interactivo hecho con Streamlit, con
  filtros por equipo y edición del Mundial.

## Instalación ##

pip install -r requirements.txt

## Ejecución ##

Pipeline completo (descarga, limpieza, EDA, consultas y gráficas):

python src/main.py

## Notebooks: ##

jupyter notebooks: 01_EDA.ipynb y 02_Visualizacion.ipynb

## Dashboard interactivo (Streamlit): ##

streamlit run dashboard/app.py

## Clases principales ##

| Clase | Responsabilidad |
|---|---|
| `CargadorDatos` | Descarga el CSV, filtra Copa Mundial, guarda en raw/processed |
| `GestorPartidos` | Consultas: get_partido, get_por_equipo, get_por_anio, get_por_sede, ventaja_local, tabla_diferencia_goles |
| `ProcesadorEDA` | limpieza_datos, agregar_columnas_derivadas, resumen_descriptivo, matriz_correlacion, desempeno_pais_sede |
| `Visualizador` | 7 gráficas: línea, barras, histograma, heatmap, scatter |
| `Utilidades` | Funciones auxiliares (validaciones, formateo) |

## Hallazgos ##

- **Ventaja del anfitrión:** el equipo que juega como país anfitrión gana
  el 62% de sus partidos, frente a un 43.5% del resto de locales, casi
  19 puntos porcentuales de diferencia, lo que sugiere que jugar frente
  a la propia afición tiene un impacto real y medible en el resultado.


- **Dominio histórico de Brasil y Alemania:** con una diferencia de goles
  acumulada de +136 y +108 respectivamente, ambas selecciones superan
  ampliamente al resto del ranking histórico (el tercer lugar, Francia,
  tiene +62), confirmando su estatus como las potencias más consistentes
  en la historia de los Mundiales.


- **Evolución del nivel de goleo:** el promedio de goles por partido
  alcanzó su punto máximo histórico en 1954 (5.38 goles/partido) y ha
  mostrado una tendencia decreciente desde entonces, estabilizándose
  entre 2.2 y 2.9 goles por partido en las ediciones más recientes,
- reflejo de un fútbol moderno más táctico y defensivo comparado con
  las primeras décadas del torneo.


- **Ventaja de local general:** más allá del caso específico del
  anfitrión, el equipo local gana el 45.85% de los partidos (frente a
  31.6% del visitante y el resto en empates), confirmando que el
  factor local es relevante incluso sin jugar en el propio país.


- **Goleadas históricas atípicas:** el análisis de outliers identificó
  partidos con marcadores muy por encima del promedio, como Suiza 7-5
  Austria (1954) y Hungría 10-1 El Salvador (1982), resultados que
  siguen siendo récords o casi récords en la historia del torneo.

## Autor ##
Gabriel Solano Molina