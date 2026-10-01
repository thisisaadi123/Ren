def validate(head):
    assert isinstance(head, list) and 1 <= len(head) <= 100_000, "1 <= n <= 10^5"
    assert all(type(v) is int and 0 <= v <= 9 for v in head), "0 <= node value <= 9"
    assert head[0] != 0 or len(head) == 1, "no leading zeros"
