import os
import glob
import csv
from os import path

from src.stats import Stats


def load_db(db_path: str, name: str) -> list[Stats]:
    data = []
    csv_files = glob.glob(os.path.join(db_path, f"{name}*.csv"))
    for csv_file in csv_files:
        season = int(csv_file.split("season_")[-1].split(".csv")[0])
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                stats = Stats(row, season)
                data.append(stats)
    return data


class SeasonDB:
    def __init__(self):
        project_root = path.dirname(path.dirname(path.abspath(__file__)))

        dbs_dir = path.join(project_root, "db")

        self.seasons = load_db(dbs_dir, "season")
        self.roster = load_db(dbs_dir, "roster")
        actual_season = max(entry.season for entry in self.seasons)
        self.season_fa = self.find_season_fa(actual_season)

    def find_player_seasons(self, uid: str) -> list[Stats]:
        player_seasons = []
        for entry in self.seasons:
            if entry.uid == uid:
                player_seasons.append(entry)
        return player_seasons

    def find_season_fa(self, season: int) -> list[Stats]:
        season_roster = []
        for entry in self.seasons:
            if entry.season == season:
                season_roster.append(entry)
        return season_roster
