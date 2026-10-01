def validate(flavours):
    n = len(flavours)
    assert isinstance(flavours, list) and 1 <= n <= 100_000, "1 <= flavours.length <= 10^5"
    assert all(type(v) is int and 0 <= v < n for v in flavours), "0 <= flavours[i] < flavours.length"
