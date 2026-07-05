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


    def detectar_outliers_goles(self):

        q1 = self.df["total_goles"].quantile(0.25)
        q3 = self.df["total_goles"].quantile(0.75)

        iqr = q3 - q1

        limite_inf = q1 - 1.5 * iqr
        limite_sup = q3 + 1.5 * iqr

        return self.df[
            (self.df["total_goles"] < limite_inf) |
            (self.df["total_goles"] > limite_sup)
        ]
