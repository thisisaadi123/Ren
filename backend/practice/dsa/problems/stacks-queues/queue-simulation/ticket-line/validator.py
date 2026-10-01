def validate(wants, k):
    assert isinstance(wants, list) and 1 <= len(wants) <= 100_000, "1 <= wants.length <= 10^5"
    assert all(type(v) is int and 1 <= v <= 10**5 for v in wants), "1 <= wants[i] <= 10^5"
    assert type(k) is int and 0 <= k < len(wants), "0 <= k < wants.length"
