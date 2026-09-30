def validate(head):
    assert isinstance(head, list), "head is given as a list of values"
    assert 1 <= len(head) <= 100_000, "1 to 10^5 nodes"
    assert all(type(v) is int and -10**5 <= v <= 10**5 for v in head), "-10^5 <= node value <= 10^5"
