def validate(head):
    assert isinstance(head, list), "head is given as a list of values"
    assert len(head) <= 100_000, "at most 10^5 nodes"
    assert all(type(v) is int and -1000 <= v <= 1000 for v in head), "-1000 <= node value <= 1000"
