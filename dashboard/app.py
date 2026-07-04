import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

import pandas as pd
import streamlit as st

from ingesta.cargador_datos import CargadorDatos
from gestor.gestor_partidos import GestorPartidos
from eda.procesador_eda import ProcesadorEDA
from visualizacion.visualizador import Visualizador

st.set_page_config(page_title="World Cup Insights", layout="wide")

# 1. Carga de datos #
cargador_datos = CargadorDatos(
    url_origen="https://raw.githubusercontent.com/martj42/international_results/master/results.csv",
    ruta_raw="data/raw/partidos-mundial.csv",
    ruta_processed="data/processed/partidos-mundial-procesado.csv",
)
df_procesado = cargador_datos.cargar_procesado()

st.title("World Cup Insights")
st.caption("Análisis de los partidos de la FIFA World Cup (1930-2026)")

# 2. Filtros en la barra lateral #
st.sidebar.header("Filtros")

equipos = sorted(pd.unique(df_procesado[["home_team", "away_team"]].values.ravel()).tolist())
equipo_seleccionado = st.sidebar.selectbox("Selecciona un equipo", equipos)

anios = sorted(df_procesado["anio"].unique().tolist())
anio_seleccionado = st.sidebar.selectbox("Filtrar por edición", ["Todas"] + anios)

# 3, Aplicar el filtro de año a el dataset #
if anio_seleccionado != "Todas":
    df_filtrado = df_procesado[df_procesado["anio"] == anio_seleccionado]
else:
    df_filtrado = df_procesado

# 4. Construimos las clases #
gestor = GestorPartidos(df_filtrado)
procesador = ProcesadorEDA(df_filtrado)
visualizador = Visualizador(df_filtrado, carpeta_salida="reports/figures")

# 5. Agregamos los KPIs #
ventaja = gestor.ventaja_local()

col1, col2, col3 = st.columns(3)
col1.metric("Partidos", len(df_filtrado))
col2.metric("Victorias del local", f"{ventaja['pct_victorias_local']}%")
col3.metric("Goles totales", int(df_filtrado["total_goles"].sum()))

# 6. Creamos la tabla de partidos del equipo seleccionado #
st.subheader(f"Partidos de {equipo_seleccionado}")
partidos_equipo = gestor.get_por_equipo(equipo_seleccionado)
st.dataframe(
    partidos_equipo[["date", "home_team", "away_team", "home_score", "away_score", "ganador"]],
    use_container_width=True,
)

# 7. Creamos las pestañas de gráficos #
tab1, tab2, tab3 = st.tabs(["Goles por edición", "Ventaja de local", "Diferencia de gol de equipos por edición"])

with tab1:
    tabla_promedio = procesador.promedio_goles_por_edicion()
    visualizador.goles_promedio_por_edicion(tabla_promedio)
    st.image("reports/figures/goles_promedio_por_edicion.png", use_container_width=True)

with tab2:
    tabla_sede = procesador.desempeno_pais_sede()
    visualizador.ventaja_pais_anfitrion(tabla_sede)
    st.image("reports/figures/ventaja_pais_anfitrion.png", use_container_width=True)
    st.dataframe(tabla_sede, use_container_width=True)

with tab3:
    tabla_diferencia = gestor.tabla_diferencia_goles(top_n=10)
    visualizador.top_diferencia_goles(tabla_diferencia)
    st.image("reports/figures/top_diferencia_goles.png", use_container_width=True)
    st.dataframe(tabla_diferencia, use_container_width=True)
