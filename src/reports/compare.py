import logging
from src.stats import Stats
from src.comparison.filters import get_filters, special_filters_formulas

min_minutes = 900
match_pct = 75
match_min = 3


def compare_player(player_roster: Stats, player_to_compare: Stats, match_pct: int) -> int:
    match_count = 0

    filters = get_filters(player_roster.style)

    for key in filters:
        special_filter = special_filters_formulas.get(key, None)
        value = player_roster.to_dict().get(key)
        compare_value = player_to_compare.to_dict().get(key)

        if not isinstance(value, float) or not isinstance(compare_value, float):
            logging.warning(f"Missing value for key '{key}': player_roster={
                            value}, player_to_compare={compare_value}")
            continue

        if special_filter is not None:
            value = value * (match_pct / 100)
            result = special_filter(player_roster.get(key), player_to_compare.get(key))
            if result:
                match_count += 1
            continue

        value = value * (match_pct / 100)

        if compare_value > value:
            match_count += 1

    return match_count


# LOGIC FOR WAGE CONVERSION TO USE LATER
# import re
# def get_wage(stats: Stats) -> int
#     match = re.search(r"[\d,]+", stats.get("Wage", "0"))
#     wage = match.group(0) if match else "0"
#
#     if not stats.get("Min WD") == "N/A":
#         match = re.search(r"[\d,]+", stats.get("Min WD", "0"))
#         wage = match.group(0) if match else "0"
#     return wage


def find_similar_players(player: Stats, db: list[Stats]) -> list[dict]:
    if player.minutes < min_minutes:
        logging.warning(f"skipping player {player.name}")
        return []

    # if player.style not in ["wb", "w", "iw", "st"]:
    # if player.style not in ["st"]:
        # logging.warning(f"not in style skipping player {player.name}")
        # return []
    print(player.name)

    matched_players = []
    for entry in db:
        if entry.minutes < min_minutes:
            continue
        score_match = compare_player(player, entry, match_pct)
        if score_match >= match_min:
            matched_players.append(entry.to_dict())
    return matched_players
