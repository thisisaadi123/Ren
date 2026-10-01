def validate(changes, target):
    assert isinstance(changes, list) and 1 <= len(changes) <= 100_000, "1 <= changes.length <= 10^5"
    assert all(type(v) is int and -10**5 <= v <= 10**5 for v in changes), "-10^5 <= changes[i] <= 10^5"
    assert type(target) is int and 1 <= target <= 10**9, "1 <= target <= 10^9"
