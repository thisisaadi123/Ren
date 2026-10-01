def validate(noise, k, limit):
    assert isinstance(noise, list) and 1 <= len(noise) <= 100_000, "1 <= noise.length <= 10^5"
    assert all(type(v) is int and 0 <= v <= 10**4 for v in noise), "0 <= noise[i] <= 10^4"
    assert type(k) is int and 1 <= k <= len(noise), "1 <= k <= noise.length"
    assert type(limit) is int and 0 <= limit <= 10**4, "0 <= limit <= 10^4"
