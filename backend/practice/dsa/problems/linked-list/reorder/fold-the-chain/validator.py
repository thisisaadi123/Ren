def validate(head):
    assert isinstance(head, list), "head is given as a list of values"
    assert len(head) <= 100_000, "at most 10^5 nodes"
    assert all(type(v) is int and -10**6 <= v <= 10**6 for v in head), "-10^6 <= node value <= 10^6"
