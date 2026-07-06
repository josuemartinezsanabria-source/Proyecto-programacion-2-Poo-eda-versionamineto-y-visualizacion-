import Clases as cl
from Clases import GestorPartidos, EDA

URL = "https://raw.githubusercontent.com/martj42/international_results/master/results.csv"
cargar_datos = cl.CargarDatos(URL)
cargar_datos.descargar_datos()
cargar_datos.filtrar_mundiales()

# Procesar datos
eda = EDA(cargar_datos.df)
eda.limpieza_datos()
eda.crear_columnas_derivadas()


#Gestor
gestor = GestorPartidos(eda.df)

print("PRUEBAS")

print("Cantidad de partidos:", len(eda.df))


if (eda.df["tournament"] == "FIFA World Cup").all():
    print(" Solo hay partidos de Mundial")
else:
    print("Existen partidos que no son del Mundial")
print("\nPrimer partido:")
print(
    gestor.get_partidos(0)[
        ["date", "home_team", "away_team"]
    ]
)

brasil = gestor.get_por_equipo("Brazil")

print(
    "\nPartidos de Brasil:",
    len(brasil)
)


partidos_2018 = gestor.get_por_año(2018)

print(
    "\nPartidos Mundial 2018:",
    len(partidos_2018)
)


print(
    "\nVentaja local:",
    round(
        gestor.ventaja_local() * 100,
        2
    ),
    "%"
)

#Mundial con mas goles

promedios = (
    eda.df.groupby("year")
    ["total_goals"]
    .mean()
    .sort_values(ascending=False)
)

print("\nMundial con más goles:")

print(promedios.head(1))

#Top goleados
print("\nTop 5 goleadas:")

print(
    eda.df.sort_values(
        "goal_difference",
        ascending=False
    )[
        [
            "home_team",
            "away_team",
            "home_score",
            "away_score"
        ]
    ].head()
)

