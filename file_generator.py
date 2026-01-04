from jinja2 import Template
import os

details_columns = ["uid", "name", "position", "club", "nat", "age", "height", "weight", "transfer_value", "wage", "expires", "personality", "season", "mins"]

gk_columns = [
    "clean_sheets",
    "cln_90",
    "con_90",
    "pens_saved",
    "pens_saved_ratio",
    "sv_pct",
    "xsv_pct",
    "svh",
    "svp",
    "svt",
]

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


def generate_html(player_compared: dict, matched_players: list[dict]) -> str:
    column_groups = [
        ("Details", details_columns),
        ("GK", gk_columns),
        ("DEF", def_columns),
        ("Poss", poss_columns),
        ("Atck", atck_columns),
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
