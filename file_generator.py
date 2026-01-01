from jinja2 import Template

details_columns = ["uid", "name", "position", "club", "nat", "age", "height", "weight", "transfer_value", "wage", "expires" "personality", "season", "mins", "]

gk_columns = [
    "clean_sheets"
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
    "defensive_score",
    "int_ratio",
    "poss_won_90",
    "int_90",
    "hdr_pct",
    "hdrs_w_90",
    "clr_90",
    "blk_90",
    "tck_w",
    "tck_r",
]

poss_columns = [
    "possession_score",
    "pres_a_90",
    "pres_c_90",
    "poss_lost_90",
    "pr_passes_90",
    "pas_pct",
    "pas_a_90",
    "xa_90",
    "drb_90",
]

atck_columns = [
    "gls",
    "gls_90",
    "np_xg",
    "np_xg_90",
    "asts_90",
    "crs_a_90",
    "xpg_diff_90",
]


def generate_html(player_compared: dict, matched_players: list[dict]) -> str:
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
        <tr><td>{{ player_compared.get(key, "") }}</td></tr>
        {% for player in matched_players %}
          <tr>
            {% for key in all_keys %}
              <td>{{ player.get(key, "") }}</td>
            {% endfor %}
          </tr>
        {% endfor %}
      </tbody>
    </table>
    """
    template = template.Template(player_compared, matched_players, details_columns, gk_columns, def_columns, poss_columns, atck_columns)

    os.makedirs("output", exist_ok=True)
    with open(f"output/report_season_{player_compared['season']_{player_compared['style']_{player_compared['name']}.html", "w", encoding="utf-8") as f:
        f.write(html_content)


