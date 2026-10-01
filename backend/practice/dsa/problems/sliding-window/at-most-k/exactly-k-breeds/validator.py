def validate(pens, k):
    n = len(pens)
    assert isinstance(pens, list) and 1 <= n <= 100_000, "1 <= pens.length <= 10^5"
    assert all(type(v) is int and 1 <= v <= n for v in pens), "1 <= pens[i] <= pens.length"
    assert type(k) is int and 1 <= k <= n, "1 <= k <= pens.length"
