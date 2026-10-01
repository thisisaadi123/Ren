def validate(codes):
    assert isinstance(codes, list) and 1 <= len(codes) <= 100_000, "1 <= codes.length <= 10^5"
    assert all(type(v) is int and -10**9 <= v <= 10**9 for v in codes), "-10^9 <= codes[i] <= 10^9"
    assert all(codes[i] < codes[i + 1] for i in range(len(codes) - 1)), "codes is strictly increasing"
