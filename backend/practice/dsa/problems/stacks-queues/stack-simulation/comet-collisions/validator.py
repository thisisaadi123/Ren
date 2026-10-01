def validate(comets):
    assert isinstance(comets, list) and 2 <= len(comets) <= 100_000, "2 <= comets.length <= 10^5"
    assert all(type(v) is int and -1000 <= v <= 1000 and v != 0 for v in comets), "-1000 <= comets[i] <= 1000, not 0"
