from jinja2 import Template
import os
import csv

details_columns = ["name","age", "wage", "height", "season", "mins", "dist_90", "position", "club", "nat", "personality", "weight", "transfer_value", "expires"]

offensive_columns = ["turn_diff", "poss_won_90", "poss_lost_90", "pr_passes_90", "pas_pct", "pas_a_90", "xa_90", "drb_90", "cr_c_90", "crs_a_90", "crs_pct", "xpg_diff", "shot_pct", "shot_pct", "hdrs_w_90", "sprint_90", "off", "off_90", "np_xg_90", "gls_90", "xgp", "xgp_90"]

<<<<<<< Updated upstream
def_columns = [
    "poss_won_90",
    "clr_90",
    "int_90",
    "hdr_pct",
    "hdrs_w_90",
    "clr_90",
    "blk_90",
    "tck_w",
    "tck_r",
    "dist_90",
]

poss_columns = [
    "pres_a_90",
    "pres_c_90",
    "poss_lost_90",
    "pr_passes_90",
    "pas_pct",
    "ps_a_90",
    "xa_90",
    "drb_90",
]

atck_columns = [
    "kpass_90",
    "sht_90",
    "sht_pct",
    "shot_90",
    "hdrs_w_90",
    "hdr_pct",
    "gls",
    "gls_90",
    "np_xg",
    "np_xg_90",
    "asts_90",
    "crs_a_90",
    "cr_c_90",
    "xpg_diff_90",
]
=======
defensive_columns = ["defensive_score", "int_90", "poss_won_90", "tck_90", "tck_r", "hdr_w_90", "hdr_pct", "clr_90", "blk_90"]
>>>>>>> Stashed changes

goalkeeping_columns = ["sv_pct", "svh", "svp", "svt", "goals_against", "clean_sheets", "pen_saves", "pen_missed", "poss_lost_90", "pr_passes_90", "tck_r"]

def generate_html(player_compared: dict, matched_players: list[dict]) -> str:
    column_groups = [
        ("Details", details_columns),
        ("GK", goalkeeping_columns),
        ("DEF", defensive_columns),
        ("OFF", offensive_columns),
    ]
    all_columns = [col for _, cols in column_groups for col in cols]

    template_str = """
    <table border="1">
      <thead>
        <tr>
          {% for group, cols in column_groups %}
            <th colspan="{{ cols|length }}">{{ group }}</th>
          {% endfor %}
        </tr>
        <tr>
          {% for col in all_columns %}
            <th>{{ col }}</th>
          {% endfor %}
        </tr>
      </thead>
      <tbody>
        <tr>
          {% for col in all_columns %}
            <td>{{ player_compared.get(col, "") }}</td>
          {% endfor %}
        </tr>
        {% for player in matched_players %}
          <tr>
            {% for col in all_columns %}
              <td>{{ player.get(col, "") }}</td>
            {% endfor %}
          </tr>
        {% endfor %}
      </tbody>
    </table>
    """

    template = Template(template_str)
    html = template.render(
        player_compared=player_compared,
        matched_players=matched_players,
        column_groups=column_groups,
        all_columns=all_columns,
    )

    os.makedirs("output", exist_ok=True)
    with open(
        f"output/report_season_{player_compared['season']}_{player_compared['style']}_{player_compared['name']}.html",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(html)


def generate_csv(player_compared: dict, matched_players: list[dict]) -> str:
    column_groups = [
        ("Details", details_columns),
        ("GK", goalkeeping_columns),
        ("DEF", defensive_columns),
        ("Atck", offensive_columns),
    ]
    all_columns = [col for _, cols in column_groups for col in cols]

    os.makedirs("output", exist_ok=True)
    csv_path = (
        f"output/report_season_{player_compared['season']}_{player_compared['style']}_{player_compared['name']}.csv"
    )
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        # Write header rows
        # First row: group names
        group_row = []
        for group, cols in column_groups:
            group_row.extend([group] * len(cols))
        writer.writerow(group_row)
        # Second row: column names
        writer.writerow(all_columns)
        # Write player_compared row
        writer.writerow([player_compared.get(col, "") for col in all_columns])
        # Write matched_players rows
        for player in matched_players:
            writer.writerow([player.get(col, "") for col in all_columns])
    return csv_path
