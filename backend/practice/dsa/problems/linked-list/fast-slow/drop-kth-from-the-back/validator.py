def validate(head, k):
    assert isinstance(head, list), "head is given as a list of values"
    assert 1 <= len(head) <= 100_000, "1 <= n <= 10^5"
    assert all(type(v) is int and -10**6 <= v <= 10**6 for v in head), "-10^6 <= node value <= 10^6"
    assert type(k) is int and 1 <= k <= len(head), "1 <= k <= n"
