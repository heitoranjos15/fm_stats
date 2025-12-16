def possession_factor(per_90_stat, possession: int) -> float:
    return per_90_stat / (100 - possession) * 50
