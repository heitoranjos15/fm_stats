
def gk_sk_filters():
    offensive_filters = [
        "poss_lost_90", "pr_passes_90"]
    defensive_filters = [
        "sv_pct", "svh", "svp", "svt", "tck_r"]
    return {"off": offensive_filters, "def": defensive_filters}


def cb_filters():
    offensive_filters = [
        "drb_90", "pas_pct", "poss_lost_90"]
    defensive_filters = [
        "poss_won_90", "hdrs_w_90", "tck_r", "int_90"]
    # return {"off": offensive_filters, "def": defensive_filters}
    return {"def": defensive_filters}

def dm_filters():
    offensive_filters = ["pas_pct", "pr_passes_90","poss_lost_90", "tck_r", "hdr_pct", "int_90"]
    return {"def": offensive_filters}

def wb_filters():
    offensive_filters = ["pr_passes_90", "drb_90", "xa_90"]
    defensive_filters = ["int_90", "tck_w", "poss_won_90"]
    return {"off": offensive_filters, "def": defensive_filters}
    # return {"off": offensive_filters}


def mc_filters():
    offensive_filters = ["pas_pct", "shot_pct", "tck_r"]
    defensive_filters = ["int_90", "tck_w", "poss_won_90", "pres_a_90"]
    # return {"off": offensive_filters, "def": defensive_filters}
    return {"def": defensive_filters}


def ms_filters():
    offensive_filters = ["pas_pct", "xa_90", "xpg_diff_90", "poss_lost_90"]
    defensive_filters = ["tck_w", "poss_won_90"]
    # return {"off": offensive_filters, "def": defensive_filters}
    return {"off": offensive_filters}


def f9_filters():
    offensive_filters = ["pas_pct", "drb_90", "xa_90"]
    defensive_filters = ["tck_w", "poss_won_90", "pres_a_90"]
    # return {"off": offensive_filters, "def": defensive_filters}
    return {"off": offensive_filters}

def wp_filters():
    offensive_filters = ["pas_pct", "drb_90", "xa_90", "poss_lost_90"]
    return {"off": offensive_filters}


def raumdeuter_filters():
    offensive_filters = ["pas_pct", "drb_90", "shot_pct", "hdrs_w_90", "xpg_diff_90"]
    defensive_filters = ["int_90", "tck_w", "poss_won_90"]
    # return {"off": offensive_filters, "def": defensive_filters}
    return {"off": offensive_filters}


def poss_lost_90_filter(player_value, stats_value):
    return stats_value <= player_value


filters_dict = {
    "sk": gk_sk_filters,
    "cb": cb_filters,
    "dm": dm_filters,
    "wb": wb_filters,
    "mc": mc_filters,
    "ms": ms_filters,
    "wp": wp_filters,
    "f9": f9_filters,
    "rmd": raumdeuter_filters,
}

special_filters = {"poss_lost_90": poss_lost_90_filter}
