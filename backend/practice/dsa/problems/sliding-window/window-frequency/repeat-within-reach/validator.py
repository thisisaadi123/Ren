def validate(codes, k):
    assert isinstance(codes, list) and 1 <= len(codes) <= 100_000, "1 <= codes.length <= 10^5"
    assert all(type(v) is int and -10**9 <= v <= 10**9 for v in codes), "-10^9 <= codes[i] <= 10^9"
    assert type(k) is int and 0 <= k <= 100_000, "0 <= k <= 10^5"
