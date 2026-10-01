def validate(stones, k):
    assert isinstance(stones, list) and 1 <= len(stones) <= 100_000, "1 <= stones.length <= 10^5"
    assert all(type(v) is int and -10**4 <= v <= 10**4 for v in stones), "-10^4 <= stones[i] <= 10^4"
    assert type(k) is int and 1 <= k <= 100_000, "1 <= k <= 10^5"
