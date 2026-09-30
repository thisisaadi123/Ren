def validate(head):
    assert isinstance(head, list), "head is given as a list of values"
    assert len(head) <= 50_000, "at most 5 * 10^4 nodes"
    assert all(type(v) is int and -10**9 <= v <= 10**9 for v in head), "-10^9 <= node value <= 10^9"
