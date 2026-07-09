import pandas as pd
from pathlib import Path

class CargarDatos:
    def __init__(self, url):
        self.url = "https://raw.githubusercontent.com/martj42/international_results/master/results.csv"
        self.df = None

    def descargar_datos(self):
        self.df = pd.read_csv(self.url)
        return self.df
    def filtrar_mundiales(self):
        self.df = self.df[
            self.df["tournament"] == "FIFA World Cup"
        ].copy()
        return self.df

    def guardar_raw(self, ruta="data/raw/partidos-mundial.csv"):
        Path(ruta).parent.mkdir(parents=True, exist_ok=True)
        self.df.to_csv(ruta, index=False)

    def guardar_procesado(
            self,
            ruta_csv="data/processed/partidos-mundial-procesado.csv",
            ruta_json="data/processed/partidos-mundial-procesado.json"
    ):
        Path(ruta_csv).parent.mkdir(parents=True, exist_ok=True)
        self.df.to_csv(ruta_csv, index=False)
        self.df.to_json(ruta_json, orient="records", indent=4)

class GestorPartidos:
    def __init__(self,df):
        self.df = df
    def get_partidos(self, indice):
        return self.df.iloc[indice]
    def get_por_equipo(self,equipo):

        return self.df[
            (self.df["home_team"]== equipo) |
            (self.df["away_team"]== equipo)
        ]
    def get_por_año(self,año):
        return self.df[
            self.df["year"]== año
        ]
    def get_por_sede(self,pais):
        return self.df[
            self.df["country"]== pais
        ]
    def ventaja_local(self):
        victorias_local = (
            self.df["home_score"]>
            self.df["away_score"]
        ).sum()
        return victorias_local / len(self.df)
    def get_por_ganador(self, equipo):
        return self.df[
            self.df["winner"]==equipo
        ]

    def get_por_ganador(self, equipo):
        return self.df[
        self.df["winner"] == equipo]


    def top_goleadas(self, n=10):
         return self.df.sort_values(
           "goal_difference",
        ascending=False
        ).head(n)
class EDA:
    def __init__(self, df):
        self.df = df.copy()
    def limpieza_datos(self):
        self.df.drop_duplicates(inplace=True)
        self.df.dropna(
            subset=[
                "date",
                "home_team",
                "away_team"],
            inplace=True)
        self.df["date"] = pd.to_datetime(self.df["date"])
        return self.df

    def crear_columnas_derivadas(self):
        self.df["year"] = self.df["date"].dt.year
        self.df["total_goals"] = (
                self.df["home_score"] +
                self.df["away_score"]
        )
        self.df["goal_difference"] = (
            abs(
                self.df["home_score"] -
                self.df["away_score"]
            )
        )

        def ganador(row):
            if row["home_score"] > row["away_score"]:
                return "Local"
            elif row["home_score"] < row["away_score"]:
                return "Visitante"
            return "Empate"
        self.df["winner_type"] = self.df.apply(
            ganador,
            axis=1
        )

        return self.df

    def matriz_correlacion(self):
        """
        Calcula la matriz de correlación requerida por el script de pruebas.
        """
        columnas = ["home_score", "away_score", "total_goals", "goal_difference"]
        return self.df[columnas].corr()

    def detectar_outliers_goles(self):

        q1 = self.df["total_goals"].quantile(0.25)
        q3 = self.df["total_goals"].quantile(0.75)

        iqr = q3 - q1

        limite_inf = q1 - 1.5 * iqr
        limite_sup = q3 + 1.5 * iqr

        return self.df[
            (self.df["total_goals"] < limite_inf) |
            (self.df["total_goals"] > limite_sup)
        ]

# =====================================================================
# MODULO 5: VISUALIZACION DE DATOS
# =====================================================================
import matplotlib.pyplot as plt
import seaborn as sns


class Visualizador:
    def __init__(self, df):
        """
        Inicializa la clase con el conjunto de datos procesado.
        """
        self.df = df
        sns.set_theme(style="whitegrid")

    def graficar_ventaja_local(self):
        """
        1. GRAFICO DE BARRAS: Analizar la distribucion de ganadores.
        """
        plt.figure(figsize=(8, 5))
        paleta = ["#FFAAA6", "#D6A2E8", "#836FA9"]

        # Se agrega hue y legend=False para evitar la advertencia en consola
        sns.countplot(data=self.df, x="winner_type", order=["Local", "Visitante", "Empate"], palette=paleta,
                      hue="winner_type", legend=False)

        plt.title("¿Existe la Ventaja Local? (Distribución de Ganadores)", fontsize=13, fontweight='bold',
                  color="#4A4A4A")
        plt.xlabel("Tipo de Ganador", fontsize=11)
        plt.ylabel("Cantidad de Partidos", fontsize=11)
        plt.tight_layout()
        plt.show()

    def graficar_goles_por_mundial(self):
        """
        2. HISTOGRAMA: Analizar la frecuencia del total de goles anotados.
        """
        plt.figure(figsize=(9, 5))

        sns.histplot(data=self.df, x="total_goals", kde=True, color="#9EEAFB", bins=12, edgecolor="#88D4E6")

        plt.title("Distribución de Goles por Partido en la Historia de los Mundiales", fontsize=13, fontweight='bold',
                  color="#4A4A4A")
        plt.xlabel("Total de Goles en un Partido", fontsize=11)
        plt.ylabel("Frecuencia (Cantidad de Partidos)", fontsize=11)
        plt.tight_layout()
        plt.show()

    def graficar_goles_local_vs_visitante(self):
        """
        3. SCATTER PLOT: Relación de goles con una línea diagonal limpia de referencia.
        """
        plt.figure(figsize=(8, 6))

        # Puntos en un azul bonito con bordes negros bien definidos
        sns.scatterplot(data=self.df, x="home_score", y="away_score", alpha=0.6, color="#1F77B4", s=130,
                        edgecolor="black")

        # --- LÍNEA DIAGONAL PERFECTA ---
        plt.plot([0, 10], [0, 10], color="#D62728", linestyle="--", linewidth=2.5, label="Línea de Empate")

        plt.title("Relación de Goles: Equipos Locales vs. Visitantes", fontsize=13, fontweight='bold', color="#4A4A4A")
        plt.xlabel("Goles del Equipo Local", fontsize=11)
        plt.ylabel("Goles del Equipo Visitante", fontsize=11)

        plt.xlim(-0.5, 10.5)
        plt.ylim(-0.5, 10.5)
        plt.legend(loc="upper right")
        plt.tight_layout()
        plt.show()

    def graficar_matriz_correlacion(self, matriz_corr):
        """
        4. HEATMAP CORREGIDO: Muestra relaciones legibles con nombres en español y alta claridad.
        """
        plt.figure(figsize=(8, 6))

        # Traducimos las etiquetas directamente sobre la matriz recibida
        nombres_espanol = ["Goles Local", "Goles Visitante", "Total Goles", "Diferencia Goles"]
        matriz_relabel = matriz_corr.copy()
        matriz_relabel.index = nombres_espanol
        matriz_relabel.columns = nombres_espanol

        sns.heatmap(
            matriz_relabel,
            annot=True,
            cmap="coolwarm",
            fmt=".2f",
            linewidths=1.5,
            linecolor="white",
            annot_kws={"size": 13, "weight": "bold"},
            vmin=-1,
            vmax=1
        )

        plt.title("Matriz de Correlación: Interrelación de Variables de Goles", fontsize=13, fontweight='bold', color="#4A4A4A", pad=15)
        plt.tight_layout()
        plt.show()