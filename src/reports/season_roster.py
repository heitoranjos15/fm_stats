from season_db import SeasonDB
from compare import find_similar_players
from file_generator import generate_html, generate_csv
from stats import Stats


def compare_fa_players(player: Stats) -> list[Stats]:
    db = SeasonDB()
    roster_players = db.roster
    fa_players = db.season_fa
    match_reports = []
    for player in roster_players:
        matched_players = find_similar_players(
            player, fa_players, match_min=2)
        match_reports.append({"player": player, "matches": matched_players})

    for match in match_reports:
        player_entry = match["player"]
        matched_players = match["matches"]
        # generate_html(
        #     player_entry, matched_players
        # )
        # generate_csv(
        #     player_entry, matched_players
        # )

    # print(match_reports)
    return matched_players
