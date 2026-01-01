
def gk_sk_filters(self):
    offensive_filters = [
        "poss_lost_90", "pr_passes_90"]
    defensive_filters = [
        "sv_pct", "svh", "svp", "svt", "tck_r"]
    return {"off": offensive_filters, "def": defensive_filters}


def cb_filters(self):
    offensive_filters = [
        "drb_90", "pas_pct", "poss_lost_90"]
    defensive_filters = [
        "int_90", "hdr_pct", "tck_w", "clr_90"]
    return {"off": offensive_filters, "def": defensive_filters}


def wb_filters(self):
    offensive_filters = ["pr_passes_90", "drb_90", "xa_90"]
    defensive_filters = ["int_90", "tck_w", "poss_won_90"]
    return {"off": offensive_filters, "def": defensive_filters}


def mc_filters(self):
    offensive_filters = ["pas_a_90", "pr_passes_90", "xa_90"]
    defensive_filters = ["int_90", "tck_w", "poss_won_90", "pres_a_90"]
    return {"off": offensive_filters, "def": defensive_filters}


def ms_filters(self):
    offensive_filters = ["shot_pct", "pas_pct", "xa_90", "drb_90"]
    defensive_filters = ["tck_w", "poss_won_90"]
    return {"off": offensive_filters, "def": defensive_filters}


def f9_filters(self):
    offensive_filters = ["pas_pct", "drb_90", "xa_90", "xpg_diff_90"]
    defensive_filters = ["tck_w", "poss_won_90", "pres_a_90"]
    return {"off": offensive_filters, "def": defensive_filters}


def raumdeuter_filters(self):
    offensive_filters = ["pr_passes_90", "drb_90", "xa_90", "xpg_diff_90"]
    defensive_filters = ["int_90", "tck_w", "poss_won_90"]
    return {"off": offensive_filters, "def": defensive_filters}


def poss_lost_90_filter(player_value, stats_value):
    return stats_value <= player_value


filters_dict = {
    "sk": gk_sk_filters,
    "cb": cb_filters,
    "wb": wb_filters,
    "mc": mc_filters,
    "ms": ms_filters,
    "f9": f9_filters,
    "raumdeuter": raumdeuter_filters,
}

special_filters = {"poss_lost_90": poss_lost_90_filter}
