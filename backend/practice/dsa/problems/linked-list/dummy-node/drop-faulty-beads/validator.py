def validate(head, bad):
    assert isinstance(head, list), "head is given as a list of values"
    assert len(head) <= 100_000, "at most 10^5 beads"
    assert all(type(v) is int and 1 <= v <= 50 for v in head), "1 <= bead value <= 50"
    assert type(bad) is int and 1 <= bad <= 50, "1 <= bad <= 50"
