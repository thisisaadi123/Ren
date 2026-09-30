def validate(head, left, right):
    assert isinstance(head, list), "head is given as a list of values"
    assert 1 <= len(head) <= 100_000, "1 <= n <= 10^5"
    assert all(type(v) is int and -10**5 <= v <= 10**5 for v in head), "-10^5 <= node value <= 10^5"
    assert type(left) is int and type(right) is int and 1 <= left <= right <= len(head), "1 <= left <= right <= n"
