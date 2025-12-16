from os import path
import os
import glob
import csv
import re
from jinja2 import Template

# Setup
season_number = 1
percentage = 0.85
minutes_played = 900


lowers_comparision = ["Poss Lost/90", "NP-xG/90", "xG-OP"]
add_possession = ["Poss Lost/90", "Poss Won/90", "Pres A/90",
                  "Clr/90", "Int/90", "Shot/90", "xG-OP", "Sprints/90", "Drb/90"]


# Rec,Inf,UID,Name,Nat,2nd Nat,Age,Position,Club,Division,Wage,Mins,Height,Weight,Loan Expires,Expires,Min WD,Max AP,Max WD,Min AP,NP-xG/90,NP-xG,xGP/90,Clr/90,Int/90,Tck/90,Tck R,Tck W,Blk/90,Hdr %,Hdrs W/90,Poss Won/90,Pres A/90,Poss Lost/90,Pas %,Ps C/90,Pr passes/90,Asts/90,xA/90,Cr C/90,Drb/90,Shot %,Shot/90,ShT/90,xG/90,xG-OP,Gls/90,xG,Sprints/90


styles_comparison = {
    "gk": ["Poss Lost/90", "Poss Won/90", "Clr/90"],
    "dc": ["Hdr %", "Int/90", "Tck R"],
    "dm": ["Pas %", "Poss Lost/90", "Int/90", "Hdr %"],
    "fb": ["Tck R", "Hdr %", "Poss Won/90"],
    "wb": ["Tck R", "Pr passes/90", "xA/90"],
    "mc": ["Pas %", "Poss Lost/90", "Pr passes/90"],
    "ms": ["xA/90", "NP-xG/90"],
    "ml": ["Pas %", "Drb/90", "xA/90"],
    "mr": ["Pas %", "Pr passes/90", "xpG_diff"],
    "sc": ["Gls/90", "NP-xG/90", "xpG_diff"],
}

general_colums = ["UID", "Name", "Position", "Age", "Height", "Min WD", "Wage", "Personality",
                  "Expires", "Mins", "Club", "Division", "season", "possession"]

dna_stats = ["Pas %", "Hdr %", "Tck R", "Poss Lost/90", "Poss Won/90"]

display_columns = {
    "gk": [],
    "dc": ["Hdrs W/90", "Tck/90", "Blk/90", "Poss Won/90", "Poss Lost/90"],
    "dm": ["Tck/90", "Pr passes/90"],
    "fb": ["Pr passes/90", "Tck/90"],
    "wb": ["Tck/90", "Hdrs W/90", "Hdr %"],
    "mc": ["Drb/90", "xA/90", "Shot/90", "Shot %"],
    "ms": ["Sprints/90", "Drb/90", "Shot/90", "Shot %", "xpG_diff"],
    "ml": ["Sprints/90", "Drb/90", "Shot/90", "Shot %", "xpG_diff"],
    "mr": ["Sprints/90", "Shot/90", "Shot %"],
    "sc": ["Sprints/90", "Hdr %", "Hdrs W/90", "Shot/90", "Shot %", "Offside/90"],
    "fa": ["p/90", "Pas A", "Pr passes/90", "Hdrs W/90", "xA/90", "NP-xG/90", "Gls/90", "xG/90", "Shot/90", "Shot %", "Hdrs W/90", "Hdr %"]
}


dbs_dir = path.join(path.dirname(__file__), "db")


def load_database() -> list:
    data = []
    csv_files = glob.glob(path.join(dbs_dir, "season*.csv"))
    for csv_file in csv_files:
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            data.append(list(reader))
    return data


def load_possession_database() -> list:
    data = []
    csv_files = glob.glob(path.join(dbs_dir, "possession_season*.csv"))
    for csv_file in csv_files:
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            data.append(list(reader))
    return data


def load_roster_database(season) -> list:
    csv_file = path.join(dbs_dir, f"roster_season_{season}.csv")
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def load_fa_database() -> list:
    csv_file = path.join(dbs_dir, f"fa.csv")
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def clean_number(s):
    if isinstance(s, (int, float)):
        return s
    value = re.sub(r'[^0-9.]', '', s) if s else 0
    try:
        float_value = float(value)
        return float_value
    except ValueError:
        return 0


def possession_factor(per_90_stat, possession: int) -> float:
    return round(per_90_stat / (100 - possession) * 50, 2)


def find_player_possession(club: str, possession_db) -> int:
    # print(possession_db)
    club_possession = next(filter(lambda x: x["club"] == club, possession_db), None)
    if club_possession and club_possession.get("possession"):
        return int(club_possession.get("possession"))
    return 50  # default possession if not found


def valid_dna(player_data, stats_to_compare, percentage=0 * 7) -> bool:
    for key in dna_stats:
        player_value = clean_number(player_data.get(key))
        comparision_value = clean_number(stats_to_compare.get(key))
        if player_value <= (comparision_value * percentage):
            return False
    return True


def fa_report(fa_db) -> list:
    fa_players = []
    for player in fa_db:
        match = re.search(r"[\d,]+", player.get("Wage", "0"))
        player["Wage"] = match.group(0) if match else "0"
        if not player["Min WD"] == "N/A":
            match = re.search(r"[\d,]+", player.get("Min WD", "0"))
            player["Min WD"] = match.group(0) if match else "0"

        try:
            pas = float(player.get("Pas A", 0))
            mins = float(player.get("Mins", 1))
            passes_per_90 = round(pas / mins, 2) * 90
        except Exception:
            print(player.get("Pas A"), player.get("Mins"))
            passes_per_90 = 0
        player["p/90"] = passes_per_90

        print(player)
        if valid_dna(player, {"Pas %": 80, "Hdr %": 75, "Tck R": 75}, percentage=0.7):
            fa_players.append(player)
    return fa_players


def compare_players(season_data, possession_db, style, player_data, season) -> list:
    match_percentage = percentage
    matches_min = len(styles_comparison.get(style, []))
    comparisons = styles_comparison.get(style, [])
    player_matches = []
    for compare in season_data:
        if not valid_dna(player_data, compare):
            continue
        match = re.search(r"[\d,]+", compare.get("Wage", "0"))
        compare["Wage"] = match.group(0) if match else "0"
        if not compare["Min WD"] == "N/A":
            match = re.search(r"[\d,]+", compare.get("Min WD", "0"))
            compare["Min WD"] = match.group(0) if match else "0"

        if style == "gk" and compare.get("Position") != "GK":
            continue
        if style in ["mr", "st"]:
            expect_goals_diff = round(
                clean_number(compare.get("xG/90")) - clean_number(compare.get("Gls/90")), 2)
            if expect_goals_diff < 0:
                continue
            compare["xpG_diff"] = expect_goals_diff

        minutes_played_value = compare.get("Mins", "0").replace(',', '')
        if not minutes_played_value.isdigit():
            continue
        if minutes_played > int(minutes_played_value):
            continue
        match_count = 0
        possession_compare = find_player_possession(compare["Club"], possession_db)
        possession_player = find_player_possession(player_data["Club"], possession_db)
        for key in comparisons:

            if key == "Offside/90" and "Offside/90" not in compare:
                compare["Offside/90"] = compare.get("Offsides/90", 0) / \
                    (compare.get("Mins", 1) * 90)

            value = compare.get(key)
            if value in ["", "-"]:
                value = 0
            else:
                if not isinstance(value, (int, float)):
                    value = clean_number(compare.get(key))

            compare_value = value
            compare[key] = compare_value
            compare["possession"] = possession_compare
            compare["season"] = season

            player_value = player_data.get(key)
            if player_value == "":
                player_value = 0
            else:
                if not isinstance(player_value, (int, float)):
                    player_value = clean_number(player_data.get(key))

            if key in add_possession:
                compare_value = possession_factor(compare_value, possession_compare)
                player_value = possession_factor(player_value, possession_player)

                compare[key] = compare_value

            if key in lowers_comparision:
                if compare_value <= (player_value / match_percentage):
                    match_count += 1
            else:
                if compare_value >= (player_value * match_percentage):
                    match_count += 1

        if match_count >= matches_min:
            player_matches.append(compare)
    return player_matches


def generate_html(players, style, file_name):
    f_name = file_name.replace(" ", "_").lower()
    template_str = """
    <table border="1">
      <thead>
        <tr>
          {% for key in all_keys %}
            <th>{{ key }}</th>
          {% endfor %}
        </tr>
      </thead>
      <tbody>
        {% for player in players %}
          <tr>
            {% for key in all_keys %}
              <td>{{ player.get(key, "") }}</td>
            {% endfor %}
          </tr>
        {% endfor %}
      </tbody>
    </table>
    """
    template = Template(template_str)

    if style == "fa":
        columns = general_colums + dna_stats + display_columns["fa"]

    else:
        columns = general_colums + dna_stats + styles_comparison[style] + display_columns[style]

    html = template.render(players=players, all_keys=columns)

    os.makedirs("results", exist_ok=True)
    with open(f"results/report_season_{season_number}_{f_name}.html", "w") as f:
        f.write(html)
    print(f"HTML report generated: ./results/report_season_{season_number}_{f_name}.html")


def generate_csv(players, style, player_name):
    player_name_clean = player_name.replace(" ", "_").lower()
    print(f"Generating CSV report for {player_name_clean}")
    columns = general_colums + dna_stats + styles_comparison[style] + display_columns[style]
    os.makedirs("results", exist_ok=True)
    with open(f"results/report_season_{season_number}_{player_name_clean}.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for player in players:
            writer.writerow({col: player.get(col, "") for col in columns})
    print(f"CSV report generated: ./results/report_season_{season_number}_{player_name_clean}.csv")


def find_players(player_to_compare, style, season_db, possession_db):
    players_found = []
    for i, season in enumerate(season_db):
        if i >= len(possession_db):
            continue

        player_matches = compare_players(
            season, possession_db[i], style, player_to_compare, i)
        if player_matches:
            players_found.extend(player_matches)
    return players_found


if __name__ == "__main__":

    season_db = load_database()
    fa_db = load_fa_database()

    def get_data_from_last_season(player):
        player_stats = next(filter(lambda x: x.get("UID") == player.get("UID"), season_db[season_number]), None)
        
        if not player_stats:
            return None

        player_stats["Min WD"] = player.get("Min WD", "N/A")
        return player_stats

    player_stats = filter(lambda x: x, map(get_data_from_last_season, fa_db))

    fa_players = fa_report(player_stats)
    generate_html(fa_players, "fa", "free_agents")
    print(f"Found {len(fa_players)} free agent players matching DNA criteria.")

    # possession_db = load_possession_database()
    # players_to_compare = load_roster_database(season_number)
    #
    # for p in players_to_compare:
    #     style = p.get("style")
    #     print(f"Finding players similar to {p.get('Name')} ({style})")
    #     if minutes_played > int(p.get("Mins", "0").replace(',', '')):
    #         continue
    #     players_found = find_players(p, style, season_db, possession_db)
    #     print(f"Found {len(players_found)} similar players.")
    #     generate_html(players_found, style, p.get("Name"))
    #     generate_csv(players_found, style, p.get("Name"))
