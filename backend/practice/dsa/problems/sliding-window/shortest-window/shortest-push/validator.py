def validate(gains, target):
    assert isinstance(gains, list) and 1 <= len(gains) <= 100_000, "1 <= gains.length <= 10^5"
    assert all(type(v) is int and 1 <= v <= 10**4 for v in gains), "1 <= gains[i] <= 10^4"
    assert type(target) is int and 1 <= target <= 10**9, "1 <= target <= 10^9"
