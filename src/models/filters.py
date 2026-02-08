def lower_comparision(compare, value):
    return compare > value


def over_comparision(compare, value):
    return compare > 0


special_filters_formulas = {
    "poss_lost_90": lower_comparision,
    "NP-xG/90": lower_comparision,
    "xG-OP/OV": over_comparision,
}


class Roles:
    goalkeeper_filters = ["sv_pct", "xsv_pct", "poss_lost_90"]
    goalkeeper_columns = ["sv_pct", "svh", "svp", "svt", "goals_against",
                          "clean_sheets", "pen_saves", "pen_missed", "poss_lost_90",
                          "pr_passes_90", "tck_r"]

    cb_filters = ["tck_r", "hdrs_w_90", "hdr_pct", "poss_won_90"]
    cb_columns = ["int_90", "poss_won_90", "poss_lost_90", "turn_diff", "tck_90", "tck_r",
                  "hdrs_w_90", "hdr_pct", "clr_90", "blk_90"]

    dm_filters = ["tck_r", "pr_passes_90", "pas_pct"]
    dm_columns = ["int_90", "poss_won_90", "poss_lost_90", "turn_diff", "hdrs_w_90", "hdr_pct",
                  "tck_r", "tck_w", "pres_a_90", "pas_pct", "pr_passes_90", "long_shots_90", "xg_op"]

    fb_filters = ["tck_r", "hdr_pct", "tck_w"]
    fb_columns = ["int_90", "poss_won_90", "poss_lost_90", "turn_diff", "hdrs_w_90", "hdr_pct",
                  "tck_w", "tck_r", "pres_a_90", "pas_pct", "pr_passes_90"]

    wb_filters = ["xa_90", "pr_passes_90", "tck_r"]
    wb_columns = ["int_90", "poss_won_90", "poss_lost_90", "turn_diff", "tck_w", "tck_r",
                  "xa_90", "crs_a_90", "crs_pct", "pr_passes_90",
                  "drb_90", "turn_diff"]

    winger_filters = ["drb_90", "xa_90", "crs_pct", "kpass"]
    winger_columns = ["drb_90", "xa_90", "crs_pct", "poss_lost_90",
                      "pr_passes_90", "pas_pct", "turn_diff", "kpass"]

    st_filters = ["xg_op", "hdrs_w_90", "drb_90"]
    st_columns = ["gls_90", "xg_90", "xg_op" , "xa_90", "hdr_pct", "hdrs_w_90",
                  "shot_pct", "shot_90", "xg_shot", "drb_90", "pas_pct", "poss_lost_90", "turn_diff", "long_shots_90"]




def get_filters(role: str) -> dict:
    role_map = {
        "gk": Roles.goalkeeper_filters,
        "sk": Roles.goalkeeper_filters,
        "w": Roles.winger_filters,
        "iw": Roles.winger_filters,

        "cb": Roles.cb_filters,
        "fb": Roles.fb_filters,
        "dm": Roles.dm_filters,
        "wb": Roles.wb_filters,
        "winger": Roles.winger_filters,
        "st": Roles.st_filters,
    }
    return role_map.get(role.lower(), [])


def get_columns(role: str) -> list:
    default_columns = ["uid", "name", "club", "nat", "height", "age", "wage", "best_pos", "minutes"]
    role_map = {
        "gk": Roles.goalkeeper_columns,
        "sk": Roles.goalkeeper_columns,
        "w": Roles.winger_columns,
        "iw": Roles.winger_columns,

        "cb": Roles.cb_columns,
        "fb": Roles.fb_columns,
        "dc": Roles.cb_columns,
        "dm": Roles.dm_columns,
        "wb": Roles.wb_columns,
        "st": Roles.st_columns,
    }
    default_columns.extend(role_map.get(role.lower(), []))
    return default_columns
