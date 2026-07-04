import os
from os import makedirs

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style = 'whitegrid')

# Esta clase genera gráfica que comunican hallazgos sobre los partidos de la FIFA World Cup #
class Visualizador:
    def __init__(self, df, carpeta_salida = "reports/figures"):
        self.df = df.copy()
        self.carpeta_salida = carpeta_salida
        os.makedirs(self.carpeta_salida, exist_ok = True)

    # Promedio de goles por mundial #
    def goles_promedio_por_edicion(self, promedio_por_anio):
        fig, ax = plt.subplots(figsize=(11, 5))
        ax.plot(promedio_por_anio["anio"], promedio_por_anio["promedio_goles_por_partido"],
                marker="o", color="#1f4e79")
        ax.set_title("¿En qué Mundial se metieron más goles por partido?")
        ax.set_xlabel("Edición del Mundial")
        ax.set_ylabel("Promedio de goles por partido")

        ax.set_xticks(promedio_por_anio["anio"])
        ax.set_xticklabels(promedio_por_anio["anio"], rotation=45, ha="right")

        fig.tight_layout()
        fig.savefig(os.path.join(self.carpeta_salida, "goles_promedio_por_edicion.png"), dpi=150)
        plt.close(fig)

    # ¿el pais sede gana mas?
    def ventaja_pais_anfitrion(self, tabla_desempeno):
        fig, ax = plt.subplots(figsize=(7, 5))
        sns.barplot(data=tabla_desempeno, x="condicion", y="pct_victorias",
                    hue="condicion", palette=["#c0392b", "#2874a6"], ax=ax, legend=False)
        ax.set_title("¿El país sede gana más? Ventaja del anfitrión")
        ax.set_ylabel("% de victorias como local")
        ax.set_xlabel("")

        for i, valor in enumerate(tabla_desempeno["pct_victorias"]):
            ax.text(i, valor + 1, f"{valor:.1f}%", ha="center", fontweight="bold")

        fig.tight_layout()
        fig.savefig(os.path.join(self.carpeta_salida, "ventaja_pais_anfitrion.png"), dpi=150)
        plt.close(fig)

    # ¿Qué selección tiene la mejor diferencia de goles histórica? #
    def top_diferencia_goles(self, tabla_diferencia):
        fig, ax = plt.subplots(figsize=(9, 6))
        datos = tabla_diferencia.sort_values("diferencia_goles")

        colores = ["#27ae60" if v >= 0 else "#c0392b" for v in datos["diferencia_goles"]]
        ax.barh(datos["equipo"], datos["diferencia_goles"], color=colores)

        ax.set_title("¿Qué selección tiene la mejor diferencia de goles histórica?")
        ax.set_xlabel("Diferencia de goles (goles a favor - goles en contra)")

        fig.tight_layout()
        fig.savefig(os.path.join(self.carpeta_salida, "top_diferencia_goles.png"), dpi=150)
        plt.close(fig)

    # Histograma de distribución de goles por partido #
    def distribucion_goles_partido(self):
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(self.df["total_goles"], bins=range(0, self.df["total_goles"].max() + 2),
                     color="#2874a6", ax=ax, discrete=True)
        ax.set_title("Distribución de goles totales por partido")
        ax.set_xlabel("Goles totales en el partido")
        ax.set_ylabel("Cantidad de partidos")
        fig.tight_layout()
        fig.savefig(os.path.join(self.carpeta_salida, "distribucion_goles_partido.png"), dpi=150)
        plt.close(fig)

    # Mapa de calor (Heatmap) de correlación #
    def heatmap_correlacion(self, matriz_correlacion):
        fig, ax = plt.subplots(figsize=(7, 6))
        sns.heatmap(matriz_correlacion, annot=True, cmap="coolwarm", center=0, ax=ax)
        ax.set_title("Matriz de correlación entre variables del partido")
        fig.tight_layout()
        fig.savefig(os.path.join(self.carpeta_salida, "heatmap_correlacion.png"), dpi=150)
        plt.close(fig)

    # Scatter — marcadores de local vs. visitante #
    def scatter_marcadores(self):
        fig, ax = plt.subplots(figsize=(7, 7))
        colores = {"Local": "#2874a6", "Visitante": "#c0392b", "Empate": "#7f8c8d"}

        for resultado, color in colores.items():
            subset = self.df[self.df["ganador"] == resultado]
            ax.scatter(subset["home_score"], subset["away_score"],
                       alpha=0.5, label=resultado, color=color)

        ax.set_title("Marcadores: goles del local vs. goles del visitante")
        ax.set_xlabel("Goles del equipo local")
        ax.set_ylabel("Goles del equipo visitante")
        ax.legend(title="Resultado")

        fig.tight_layout()
        fig.savefig(os.path.join(self.carpeta_salida, "scatter_marcadores.png"), dpi=150)
        plt.close(fig)

    # Países que más veces han sido sede #
    def partidos_por_pais_sede(self, top_n=10):
        conteo = self.df["country"].value_counts().head(top_n).reset_index()
        conteo.columns = ["country", "partidos"]

        fig, ax = plt.subplots(figsize=(9, 5))
        sns.barplot(data=conteo, x="partidos", y="country", hue="country",
                    palette="Blues_r", ax=ax, legend=False)
        ax.set_title(f"Top {top_n} países que más partidos han organizado")
        ax.set_xlabel("Cantidad de partidos")
        ax.set_ylabel("")

        fig.tight_layout()
        fig.savefig(os.path.join(self.carpeta_salida, "partidos_por_pais_sede.png"), dpi=150)
        plt.close(fig)
    