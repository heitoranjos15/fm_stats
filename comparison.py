import os
import glob
import csv

from filters import filters_dict, special_filters
from stats import Stats
from player import Player
from os import path


from file_generator import generate_html


def load_db(db_path: str, name: str) -> list[dict]:
    data = []
    csv_files = glob.glob(os.path.join(db_path, f"{name}*.csv"))
    for csv_file in csv_files:
        season = int(csv_file.split("season_")[-1].split(".csv")[0])
        if season > 2:
            with open(csv_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    stats = Stats(row, season)
                    data.append(stats.to_dict())
    return data


def load_possession_db(db_path) -> list:
    data = []
    csv_files = glob.glob(path.join(db_path, "possession_season*.csv"))
    for csv_file in csv_files:
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            data.append(list(reader))
    return data


def find_players(player: dict, db: list[dict], style, match_pct, match_min) -> list[Stats]:
    matched_players = []
    filter_func = filters_dict.get(style)
    if not filter_func:
        return matched_players
    filters = filter_func()

    for entry in db:
        score_match = 0
        for name, filter_keys in filters.items():
            if score_match >= match_min:
                break
            for filter in filter_keys:
                result = apply_filter(player, entry, filter, match_pct)
                if result:
                    score_match += 1
                if score_match >= match_min:
                    matched_players.append(entry)
                    break
    return matched_players


def apply_filter(player, stats, off_filter, match_pct):
    player_value = player.get(off_filter)
    stats_value = stats.get(off_filter)
    is_special_filter_func = special_filters.get(off_filter)
    if is_special_filter_func:
        return is_special_filter_func(player_value, stats_value)

    if stats_value is None or player_value is None:
        return False
    return stats_value > player_value * (match_pct / 100)


def main():
    dbs_dir = path.join(path.dirname(__file__), "db")
    season_db = load_db(dbs_dir, "season")
    roster_db = load_db(dbs_dir, "roster_season_4")

    matches = []
    for player_entry in roster_db:
        player_style = player_entry.get("style")
        match_pct = 80
        match_min = 3
        matched_players = find_players(
            player_entry, season_db, player_style, match_pct, match_min)
        if len(matched_players):
            matches.append({"player": player_entry, "matches": matched_players})

    for match in matches:
        player_entry = match["player"]
        matched_players = match["matches"]
        generate_html(
            player_entry, matched_players
        )
        print(
            f"Generated report for {player_entry.get("name")} with {len(matched_players)} matches."
        )
    print(f"All reports generated. total players: {len(roster_db)}")


if __name__ == "__main__":
    main()
