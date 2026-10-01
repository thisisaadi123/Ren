def validate(temps, k):
    assert isinstance(temps, list) and 1 <= len(temps) <= 100_000, "1 <= temps.length <= 10^5"
    assert all(type(v) is int and -10**4 <= v <= 10**4 for v in temps), "-10^4 <= temps[i] <= 10^4"
    assert type(k) is int and 1 <= k <= len(temps), "1 <= k <= temps.length"
