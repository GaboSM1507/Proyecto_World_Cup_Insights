from ingesta.cargador_datos import CargadorDatos
from eda.procesador_eda import ProcesadorEDA
from gestor.gestor_partidos import GestorPartidos
from visualizacion.visualizador import Visualizador

def main():
    # 1. Ingesta: descargar y filtra los partidos de la FIFA World Cup #
    cargador = CargadorDatos(url_origen="https://raw.githubusercontent.com/martj42/international_results/master/results.csv")
    df_crudo = cargador.descargar_y_filtrar()
    print(f"Partidos de la FIFA World Cup descargados: {len(df_crudo)}")

    # 2. EDA: limpieza y columnas derivadas
    procesador = ProcesadorEDA(df_crudo)
    procesador.limpieza_datos()
    df_procesado = procesador.agregar_columnas_derivadas()
    print(f"Partidos tras limpieza: {len(df_procesado)}")

    # 3. Persistencia del dataset procesado
    cargador.guardar_procesado(df_procesado)
    print("Dataset procesado guardado en data/processed/")

    # 4. Resumen y correlación
    print(procesador.resumen_descriptivo())
    matriz_corr = procesador.matriz_correlacion()
    print(matriz_corr)
    print(procesador.desempeno_pais_sede())

    # 5. Consultas con GestorPartidos
    gestor = GestorPartidos(df_procesado)
    print(gestor.ventaja_local())
    tabla_diferencia = gestor.tabla_diferencia_goles(top_n=10)
    print(tabla_diferencia)

    # 6. Visualización
    visualizador = Visualizador(df_procesado)
    tabla_promedio = procesador.promedio_goles_por_edicion()
    visualizador.goles_promedio_por_edicion(tabla_promedio)

    tabla_sede = procesador.desempeno_pais_sede()
    visualizador.ventaja_pais_anfitrion(tabla_sede)

    visualizador.top_diferencia_goles(tabla_diferencia)
    visualizador.distribucion_goles_partido()
    visualizador.heatmap_correlacion(matriz_corr)
    visualizador.scatter_marcadores()
    visualizador.partidos_por_pais_sede(top_n=10)

    print("Todas las gráficas fueron generadas en reports/figures/")

if __name__ == "__main__":
    main()
