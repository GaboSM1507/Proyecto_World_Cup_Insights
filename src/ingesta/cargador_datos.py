import os
import pandas as pd

# Se encarga de descargar el CSV de partidos internacionales y filtrar solo los de la FIFA World Cup #
class CargadorDatos:

    def __init__(self, url_origen, ruta_raw = "data/raw/partidos-mundial.csv", ruta_processed = "data/processed/partidos-mundial-procesado.csv"):
        self.url_origen = url_origen
        self.ruta_raw = ruta_raw
        self.ruta_processed = ruta_processed
        self.df = None

    def descargar_y_filtrar(self):
        df_completo = pd.read_csv(self.url_origen)
        df_mundial = df_completo[df_completo["tournament"] == "FIFA World Cup"].copy()

        df_mundial.reset_index(drop=True, inplace=True)
        df_mundial.insert(0, "id_partido", range(1, len(df_mundial) + 1))

        os.makedirs(os.path.dirname(self.ruta_raw), exist_ok=True)
        df_mundial.to_csv(self.ruta_raw, index=False)

        self.df = df_mundial
        return self.df

    def cargar_procesado(self):
        self.df = pd.read_csv(self.ruta_processed, parse_dates=["date"])
        return self.df

    def guardar_procesado(self, df_procesado):
        os.makedirs(os.path.dirname(self.ruta_processed), exist_ok=True)
        df_procesado.to_csv(self.ruta_processed, index=False)