def possession_factor(per_90_stat, possession: int) -> float:
    if not possession:
        possession = 50
    return per_90_stat / (100 - possession) * 50


def per_90(value: int, minutes: int, possession = 50) -> float:
    if minutes == 0:
        return 0.0
    offsides_per_90 = (value / minutes) * 90
    return possession_factor(offsides_per_90, possession)


class Stats:
    def __init__(self, data: dict, season):
        def format_string(value):
            if isinstance(value, str):
                return value.replace(",", "").replace("-", "0").replace("N/A", "0").replace("km", "").strip()
            return value

        def to_float(value):
            try:
                return float(format_string(value))
            except (ValueError, TypeError):
                return 0.0

        self.minutes = to_float(data.get("Mins", 0))
        self.clean_sheets = to_float(data.get("Clean Sheets"))
        self.cln_90 = to_float(data.get("Cln/90"))
        self.con_90 = to_float(data.get("Con/90"))
        self.xa = to_float(data.get("xA"))
        self.xa_90 = to_float(data.get("xA/90"))
        self.xg_op = to_float(data.get("xG-OP"))
        self.xg_90 = to_float(data.get("xG/90"))
        self.g_mis = to_float(data.get("G. Mis"))
        self.gls_90 = to_float(data.get("Gls/90"))
        self.conc = to_float(data.get("Conc"))
        self.gls = to_float(data.get("Gls"))
        self.mins = to_float(data.get("Mins"))
        self.np_xg = to_float(data.get("NP-xG"))
        self.np_xg_90 = to_float(data.get("NP-xG/90"))
        self.pens_faced = to_float(data.get("Pens Faced"))
        self.pens_saved = to_float(data.get("Pens Saved"))
        self.pens_saved_90 = per_90(self.pens_saved, self.minutes)
        self.pens_saved_ratio = to_float(data.get("Pens Saved Ratio"))
        self.xg = to_float(data.get("xG"))
        self.asts_90 = to_float(data.get("Asts/90"))
        self.blk = to_float(data.get("Blk"))
        self.blk_90 = to_float(data.get("Blk/90"))
        self.clear = to_float(data.get("Clear"))
        self.clr_90 = to_float(data.get("Clr/90"))
        self.conv_pct = to_float(data.get("Conv %"))
        self.cr_c_a = to_float(data.get("Cr C/A"))
        self.cr_a = to_float(data.get("Cr A"))
        self.crs_a_90 = to_float(data.get("Crs A/90"))
        self.cr_c = to_float(data.get("Cr C"))
        self.cr_c_90 = to_float(data.get("Cr C/90"))
        self.distance = to_float(data.get("Distance"))
        self.dist_90 = to_float(data.get("Dist/90"))
        self.drb = to_float(data.get("Drb"))
        self.drb_90 = to_float(data.get("Drb/90"))
        self.xg_shot = to_float(data.get("xG/shot"))
        self.xgp = to_float(data.get("xGP"))
        self.xgp_90 = to_float(data.get("xGP/90"))
        self.xsv_pct = to_float(data.get("xSv %"))
        self.hdrs = to_float(data.get("Hdrs"))
        self.hdrs_w_90 = to_float(data.get("Hdrs W/90"))
        self.hdr_pct = to_float(data.get("Hdr %"))
        self.sprints_90 = to_float(data.get("Sprints/90"))
        self.itc = to_float(data.get("Itc"))
        self.int_90 = to_float(data.get("Int/90"))
        self.off = to_float(data.get("Off"))
        self.pas_a = to_float(data.get("Pas A"))
        self.ps_a_90 = to_float(data.get("Ps A/90"))
        self.pas_pct = to_float(data.get("Pas %"))
        self.ps_c = to_float(data.get("Ps C"))
        self.ps_c_90 = to_float(data.get("Ps C/90"))
        self.poss_lost_90 = to_float(data.get("Poss Lost/90"))
        self.poss_won_90 = to_float(data.get("Poss Won/90"))
        self.pres_a = to_float(data.get("Pres A"))
        self.pres_c = to_float(data.get("Pres C"))
        self.pres_c_90 = to_float(data.get("Pres C/90"))
        self.pres_a_90 = to_float(data.get("Pres A/90"))
        self.pr_passes = to_float(data.get("Pr Passes"))
        self.pr_passes_90 = to_float(data.get("Pr Passes/90"))
        self.sv_pct = to_float(data.get("Sv %"))
        self.svh = to_float(data.get("Svh"))
        self.svp = to_float(data.get("Svp"))
        self.svt = to_float(data.get("Svt"))
        self.shots = to_float(data.get("Shots"))
        self.sht = to_float(data.get("ShT"))
        self.sht_90 = to_float(data.get("ShT/90"))
        self.shot_pct = to_float(data.get("Shot %"))
        self.shot_90 = to_float(data.get("Shot/90"))
        self.tck_r = to_float(data.get("Tck R"))
        self.tck_a = to_float(data.get("Tck A"))
        self.tck_w = to_float(data.get("Tck W"))
        self.tck_90 = to_float(data.get("Tck/90"))

        # self.pres_a_90 = possession_factor(data.get("Pres A/90"), possession)
        # self.pr_passes_90 = possession_factor(data.get("Pr passes/90"), possession)

        self.tck_w_90 = per_90(self.tck_w, self.mins)
        self.off_90 = per_90(self.off, self.minutes)

        self.turn_diff = self.poss_won_90 - self.poss_lost_90
        self.xpg_diff = self.gls_90 - self.xg_90

        self.defensive_score = (
            self.int_90 + self.clr_90 + self.blk_90 + self.tck_90
        ) / 4
        self.int_ratio = self.int_90 / self.defensive_score
        self.possession_score = (
            self.poss_won_90 + self.pr_passes_90 + self.pres_a_90
        ) / 3
        self.offensive_score = (
            self.asts_90 + self.gls_90 + self.crs_a_90 + self.xa_90
        ) / 4

    def to_dict(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "position": self.position,
            "club": self.club,
            "nat": self.nat,
            "height": self.height,
            "weight": self.weight,
            "age": self.age,
            "transfer_value": self.transfer_value,
            "wage": self.wage,
            "best_pos": self.best_pos,
            "ability": self.ability,
            "clean_sheets": self.clean_sheets,
            "cln_90": self.cln_90,
            "con_90": self.con_90,
            "xa": self.xa,
            "xa_90": self.xa_90,
            "xg_op": self.xg_op,
            "xg_90": self.xg_90,
            "g_mis": self.g_mis,
            "gls_90": self.gls_90,
            "conc": self.conc,
            "gls": self.gls,
            "mins": self.mins,
            "np_xg": self.np_xg,
            "np_xg_90": self.np_xg_90,
            "pens_faced": self.pens_faced,
            "pens_saved": self.pens_saved,
            "pens_saved_ratio": self.pens_saved_ratio,
            "xg": self.xg,
            "asts_90": self.asts_90,
            "blk": self.blk,
            "blk_90": self.blk_90,
            "clear": self.clear,
            "clr_90": self.clr_90,
            "conv_pct": self.conv_pct,
            "cr_c_a": self.cr_c_a,
            "cr_a": self.cr_a,
            "crs_a_90": self.crs_a_90,
            "cr_c": self.cr_c,
            "cr_c_90": self.cr_c_90,
            "distance": self.distance,
            "dist_90": self.dist_90,
            "drb": self.drb,
            "drb_90": self.drb_90,
            "xg_shot": self.xg_shot,
            "xgp": self.xgp,
            "xgp_90": self.xgp_90,
            "xsv_pct": self.xsv_pct,
            "hdrs": self.hdrs,
            "hdrs_w_90": self.hdrs_w_90,
            "hdr_pct": self.hdr_pct,
            "sprints_90": self.sprints_90,
            "itc": self.itc,
            "int_90": self.int_90,
            "off": self.off,
            "pas_a": self.pas_a,
            "ps_a_90": self.ps_a_90,
            "pas_pct": self.pas_pct,
            "ps_c": self.ps_c,
            "ps_c_90": self.ps_c_90,
            "poss_lost_90": self.poss_lost_90,
            "poss_won_90": self.poss_won_90,
            "pres_a": self.pres_a,
            "pres_a_90": self.pres_a_90,
            "pres_c": self.pres_c,
            "pres_c_90": self.pres_c_90,
            "pr_passes": self.pr_passes,
            "pr_passes_90": self.pr_passes_90,
            "sv_pct": self.sv_pct,
            "svh": self.svh,
            "svp": self.svp,
            "svt": self.svt,
            "shots": self.shots,
            "sht": self.sht,
            "sht_90": self.sht_90,
            "shot_pct": self.shot_pct,
            "shot_90": self.shot_90,
            "tck_r": self.tck_r,
            "tck_a": self.tck_a,
            "tck_w": self.tck_w,
            "tck_90": self.tck_90,
            "turn_diff": self.turn_diff,
            "xpg_diff": self.xpg_diff,
            "defensive_score": self.defensive_score,
            "possession_score": self.possession_score,
            "offensive_score": self.offensive_score,
            "int_ratio": self.int_ratio,
        }

