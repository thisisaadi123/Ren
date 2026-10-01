def validate(prefers, trays):
    assert isinstance(prefers, list) and 1 <= len(prefers) <= 100_000, "1 <= prefers.length <= 10^5"
    assert isinstance(trays, list) and len(trays) == len(prefers), "prefers and trays have the same length"
    assert all(v in (0, 1) and type(v) is int for v in prefers + trays), "values are 0 or 1"
