class Player:
    def __init__(self, data: dict, season):
        def format_wage(value):
            if isinstance(value, str):
                return value.replace("€", "").replace("N/A", "0").replace("-", "0").replace(",", "").replace("p/w", "").strip()
            return value
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
        self.style = data.get("style")

    def to_dict(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "position": self.position,
            "club": self.club,
            "nat": self.nat,
            "age": self.age,
            "height": self.height,
            "weight": self.weight,
            "transfer_value": self.transfer_value,
            "wage": self.wage,
            "best_pos": self.best_pos,
            "season": self.season,
            "style": self.style,
        }

