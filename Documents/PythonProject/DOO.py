from collections import defaultdict
from dataclasses import dataclass

@dataclass
class Partido:
    date: int
    home_team: str
    away_team: str
    tournament: str
    city: str
    country: str
    neutral: bool

class Equipo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.partidos = []

    def add_partido(self, partido):
        self.partidos.append(partido)

    def total_partidos(self):
        return len(self.partidos)

import pandas as pd
from matches import Match

@dataclass
class Match:
    date: str
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    tournament: str
    city: str
    country: str
    neutral: bool

class CSV:
    def load_match(self, filepath):
        df = pd.read_csv("Resultados partidos internacionales.csv")

        matches = []

        for _, row in df.iterrows():
            matches.append(
                Match(
                    date=row["date"],
                    home_team=row["home_team"],
                    away_team=row["away_team"],
                    home_score=row["home_score"],
                    away_score=row["away_score"],
                    tournament=row["tournament"],
                    city=row["city"],
                    country=row["country"],
                    neutral=row["neutral"]
                )
            )

        return matches
#Repositorio
class MatchRepository:
    def __init__(self, matches):
        self.matches = matches
    def by_team(self, team):
        return [
            m for m in self.matches
            if m.home_team == team
            or m.away_team == team
        ]
    def by_tournament(self, tournament):
        return [
            m for m in self.matches
            if m.tournament == tournament
        ]
    def by_country(self, country):
        return [
            m for m in self.matches
            if m.country == country
        ]
import collections #Total de goles
class Analisis:
    def __init__(self, matches):
        self.matches = matches
    def goals_by_equipo(self):
        goals = defaultdict(int)
        for m in self.matches:
            goals[m.home_team] += m.home_score
            goals[m.away_team] += m.away_score
        return dict(goals)
#Equipos con mas victorias
    def victorias_por_equipos(self):
        victorias = defaultdict(int)
        for m in self.matches:
            if m.home_score > m.away_score:
                victorias[m.home_team] += 1
            elif m.away_score > m.home_score:
                victorias[m.away_team] += 1
        return dict(victorias)
#Ranking historico
def historial (self):
    points = defaultdict(int)
    for m in self.matches:

        if m.home_score > m.away_score:
            points[m.home_team] += 3
        elif m.away_score > m.home_score:
            points[m.away_team] += 3
        else:
            points[m.home_team] += 1
            points[m.away_team] += 1
    return dict(points)