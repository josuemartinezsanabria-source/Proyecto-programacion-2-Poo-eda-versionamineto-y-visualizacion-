from DOO import CSV, Partido, Match

loader = CSV()
matches = loader.load_match(
    "Resultados partidos internacionales.csv"
)

print("Cantidad de partidos: ", len(matches))

print("\nPrimer partido:")
print(matches[0])

print("\nUltimo partido:")
print(matches[-1])


brasil = []

for match in matches:

    if match.home_team == "Brazil" or match.away_team == "Brazil":
        brasil.append(match)

print("Partidos de Brasil:", len(brasil))


assert len(matches) > 0

print(" Dataset cargado correctamente")

mundial = []
for match in matches:
    if match.tournament == "FIFA World Cup":
     mundial.append(match)
print("Partidos del mundial:", len(mundial))