class Stats:
    def __init__(self, data: dict, season):
        def format_string(value):
            if isinstance(value, str):
                return value.replace(",", "").replace("-", "0").replace("N/A", "0").replace("km", "").replace("%", "").strip()
            return value

        def to_float(value):
            try:
                return float(format_string(value))
            except (ValueError, TypeError):
                return 0.0

        def format_wage(value):
            if isinstance(value, str):
                return value.replace("€", "").replace("N/A", "0").replace("-", "0").replace(",", "").replace("p/w", "").strip()
            return value

        def per_90(value: int, minutes: int) -> float:
            if minutes == 0:
                return 0.0
            return round((value / minutes) * 90, 2)

        def possession_factor(per_90_stat, possession: int) -> float:
            if not possession:
                possession = 50
            return per_90_stat / (100 - possession) * 50

        self.uid = data.get("UID")
        self.name = data.get("Name")
        self.position = data.get("Position")
        self.club = data.get("Club")
        self.nat = data.get("Nat")
        self.height = data.get("Height")
        self.weight = data.get("Weight")
        self.age = data.get("Age")
        self.transfer_value = data.get("Transfer Value")
        self.wage = format_wage(data.get("Wage"))
        self.best_pos = data.get("Best Pos")
        self.style = ""
        if data.get("style"):
            self.style = data.get("style").strip()
        self.match_pct = data.get("Match Pct", 80)
        self.match_min = data.get("Match Min", 3)
        self.season = season

        self.minutes = to_float(data.get("Mins", 0))
        self.clean_sheets = to_float(data.get("Clean Sheets"))
        self.cln_90 = to_float(data.get("Cln/90"))
        self.con_90 = to_float(data.get("Con/90"))
        self.xa = to_float(data.get("xA"))
        self.xa_90 = to_float(data.get("xA/90"))
        self.xg_op = to_float(data.get("xG-OP"))  # xg overperformance
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
        self.cr_c = to_float(data.get("Cr C"))
        self.crs_a_90 = to_float(data.get("Crs A/90"))
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
        self.pres_c_90 = to_float(data.get("Ps C/90"))
        self.pres_a_90 = to_float(data.get("Ps A/90"))
        self.pr_passes = to_float(data.get("Pr Passes"))
        self.pr_passes_90 = to_float(data.get("Pr passes/90"))
        self.sv_pct = to_float(data.get("Sv %"))
        self.svh = to_float(data.get("Svh"))
        self.svp = to_float(data.get("Svp"))
        self.svt = to_float(data.get("Svt"))
        self.shots = to_float(data.get("Shots"))
        self.sht = to_float(data.get("ShT"))
        self.sht_90 = to_float(data.get("ShT/90"))
        self.shot_pct = to_float(data.get("Shot %"))
        self.shot_90 = to_float(data.get("Shot/90"))
        self.tck_r = to_float(format_string(data.get("Tck R")))
        self.tck_a = to_float(data.get("Tck A"))
        self.tck_w = to_float(data.get("Tck W"))
        self.tck_90 = to_float(data.get("Tck/90"))
        self.kpass = to_float(data.get("K Ps/90"))
        self.long_shots_90 = to_float(data.get("Shots Outside Box/90"))

        # self.pres_a_90 = possession_factor(data.get("Pres A/90"), possession)
        # self.pr_passes_90 = possession_factor(data.get("Pr passes/90"), possession)

        self.tck_w_90 = per_90(self.tck_w, self.mins)
        self.off_90 = per_90(self.off, self.minutes)
        self.pens_saved_90 = per_90(self.pens_saved, self.minutes)

        self.crs_pct = round(to_float(self.cr_a / self.cr_c) * 100 if self.cr_c > 0 else 0.0, 2)

        self.turn_diff = round(self.poss_won_90 - self.poss_lost_90, 2)

    def to_dict(self):
        return self.__dict__

    def get(self, key):
        return self.__dict__.get(key)
