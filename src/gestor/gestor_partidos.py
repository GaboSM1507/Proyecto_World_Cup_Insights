import pandas as pd

# Expone consultas de solo lectura sobre el DataFrame de partidos de la FIFA World Cup #
class GestorPartidos:
    def __init__(self, df):
        self.df = df.copy()

    def get_partido(self, id_partido):
        return self.df[self.df["id_partido"] == id_partido]

    def get_por_equipo(self, equipo):
        mascara = (self.df["home_team"] == equipo) | (self.df["away_team"] == equipo)
        return self.df[mascara]

    def get_por_anio(self, anio):
        anios = pd.to_datetime(self.df["date"]).dt.year
        return self.df[anios == anio]

    def get_por_sede(self, pais):
        return self.df[self.df["country"] == pais]

    def goles_por_equipo(self, equipo):
        partidos = self.get_por_equipo(equipo).dropna(subset=["home_score", "away_score"])

        goles_favor = (
                partidos.loc[partidos["home_team"] == equipo, "home_score"].sum()
                + partidos.loc[partidos["away_team"] == equipo, "away_score"].sum()
        )
        goles_contra = (
                partidos.loc[partidos["home_team"] == equipo, "away_score"].sum()
                + partidos.loc[partidos["away_team"] == equipo, "home_score"].sum()
        )

        return {
            "equipo": equipo,
            "goles_a_favor": int(goles_favor),
            "goles_en_contra": int(goles_contra),
            "diferencia_goles": int(goles_favor - goles_contra),
        }

    def tabla_diferencia_goles(self, top_n=10):
        equipos = pd.unique(self.df[["home_team", "away_team"]].values.ravel())

        filas = []
        for equipo in equipos:
            filas.append(self.goles_por_equipo(equipo))

        tabla = pd.DataFrame(filas).sort_values("diferencia_goles", ascending=False)
        return tabla.head(top_n).reset_index(drop=True)

    def ventaja_local(self):
        df = self.df.dropna(subset = ["home_score", "away_score"])
        local = (df["home_score"] > df["away_score"]).sum()
        visitante = (df["home_score"] < df["away_score"]).sum()
        empate = (df["home_score"] == df["away_score"]).sum()
        total = len(df)

        return {
            "victorias_local": int(local),
            "victorias_visitante": int(visitante),
            "empates": int(empate),
            "pct_victorias_local": round(local / total * 100, 2),
        }
