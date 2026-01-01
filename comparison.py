import os
import glob
import csv

from filters import filters_dict, special_filters
from stats import Stats
from os import path


from file_generator import generate_html


def load_db(db_path: str, name: str) -> list[dict]:
    data = []
    csv_files = glob.glob(os.path.join(db_path, f"{name}*.csv"))
    season = 0
    for csv_file in csv_files:
        season += 1
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                stats = Stats(row, season)
                player_details = Player()
                data.append({stats: stats, player_details: player_details})
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
    filters = filter_func()

    for entry in db:
        stats: Stats = entry["stats"]
        score_match = 0
        for name, filter in filters:
            result = apply_filter(player, stats, filter, match_pct)
            if result:
                score_match += 1
            if score_match >= match_min:
                matched_players.append({name: entry})
                break
    return matched_players


def apply_filter(player, stats, off_filter, match_pct):
    player_value = player.get(off_filter)
    stats_value = stats.get(off_filter)
    is_special_filter_func = special_filters.get(off_filter)
    if is_special_filter_func:
        return is_special_filter_func(player_value, stats_value)

    return stats_value < player_value * (match_pct / 100)


def main():
    dbs_dir = path.join(path.dirname(__file__), "db")
    season_db = load_db(dbs_dir, "season")
    roster_db = load_db(dbs_dir, "roster")

    matches = []
    for player_entry in roster_db:
        player_stats: Stats = player_entry["stats"]
        player_style = player_entry["player_details"].style
        match_pct = player_entry["player_details"].match_pct
        match_min = player_entry["player_details"].match_min
        matched_players = find_players(
            player_stats.to_dict(), season_db, player_style, match_pct, match_min)
        matches.append({"player": player_entry, "matches": matched_players})

    for match in matches:
        player_entry = match["player"]
        matched_players = match["matches"]
        player_stats: Stats = player_entry["stats"]
        player_details: Player = player_entry["player_details"]
        generate_html(
            player_stats.to_dict(), [p["stats"].to_dict() for p in matched_players],
            player_details.style
        )
        import logging
        logging.info(
            f"Generated report for {player_stats.name} with {len(matched_players)} matches."
        )
    logging.info(f"All reports generated. total players: {len(roster_db)}")


if __name__ == "__main__":
    main()
