def validate(items, k):
    assert isinstance(items, list) and 1 <= len(items) <= 100_000, "1 <= items.length <= 10^5"
    assert all(type(v) is int and 1 <= v <= 10**9 for v in items), "1 <= items[i] <= 10^9"
    assert type(k) is int and 1 <= k <= len(items), "1 <= k <= items.length"
