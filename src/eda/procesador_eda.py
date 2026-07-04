import pandas as pd
import numpy as np

# Esta clase realiza la limpieza y el análisis exploratorio del DataFrame de partidos de la FIFA World Cup #
class ProcesadorEDA:
    def __init__(self, df):
        self.df = df.copy()

    def limpieza_datos(self):
        df = self.df.copy()

        # Convierte la columna date de texto a fecha real #
        df["date"] = pd.to_datetime(df["date"], errors ="coerce")

        # Elimina partidos sin marcador #
        df = df.dropna(subset = ["home_score", "away_score", "date"])

        # Hace que los goles queden como enteros #
        df["home_score"] = df["home_score"].astype(int)
        df["away_score"] = df["away_score"].astype(int)

        # Quita duplicados exactos #
        df = df.drop_duplicates()

        # Ordena por fecha y reinicia el indice #
        df = df.sort_values("date").reset_index(drop = True)

        self.df = df
        return self.df

    def agregar_columnas_derivadas(self):
        df = self.df.copy()

        # Año de la edición del mundial #
        df["anio"] = df["date"].dt.year

        # Total de goles combinados del partido #
        df["total_goles"] = df["home_score"] + df["away_score"]

        # Diferencia de goles: positivo si ganó el local y negativo si ganó el visitante #
        df["diferencia_goles"] = df["home_score"] - df["away_score"]

        # Determina el ganador según el marcador #
        condiciones = [
            df["home_score"] > df["away_score"],
            df["home_score"] < df["away_score"],
        ]
        opciones = ["Local", "Visitante"]
        df["ganador"] = np.select(condiciones, opciones, default = "Empate")

        self.df = df
        return self.df

    def resumen_descriptivo(self):
        columnas = ["home_score", "away_score", "total_goles", "diferencia_goles"]
        return self.df[columnas].describe()

    def matriz_correlacion(self):
        columnas = ["home_score", "away_score", "total_goles", "diferencia_goles", "anio"]
        return self.df[columnas].corr()

# Metodos para analisis #

    # Desempeño del pais sede #
    def desempeno_pais_sede(self):
        df = self.df.copy()
        es_anfitrion = df["home_team"] == df["country"]

        anfitrion = df[es_anfitrion]
        resto = df[~es_anfitrion]

        pct_anfitrion = (anfitrion["home_score"] > anfitrion["away_score"]).mean() * 100
        pct_resto = (resto["home_score"] > resto["away_score"]).mean() * 100

        return pd.DataFrame([
            {"condicion": "Anfitrión jugando en casa", "pct_victorias": round(pct_anfitrion, 2)},
            {"condicion": "Resto de locales (no anfitriones)", "pct_victorias": round(pct_resto, 2)},
        ])

    # Partidos con goleadas atipicas #
    def detectar_outliers_goles(self):
        q1 = self.df["total_goles"].quantile(0.25)
        q3 = self.df["total_goles"].quantile(0.75)
        iqr = q3 - q1
        limite_superior = q3 + 1.5 * iqr

        return self.df[self.df["total_goles"] > limite_superior].sort_values(
            "total_goles", ascending=False
        )

    # Promedio de goles por mundial #
    def promedio_goles_por_edicion(self):
        return (
            self.df.groupby("anio")["total_goles"]
            .mean()
            .round(2)
            .reset_index()
            .rename(columns={"total_goles": "promedio_goles_por_partido"})
        )
