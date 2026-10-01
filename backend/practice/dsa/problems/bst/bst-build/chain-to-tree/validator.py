def validate(head):
    assert isinstance(head, list) and 1 <= len(head) <= 100_000, "1 <= n <= 10^5"
    assert all(type(v) is int and -10**9 <= v <= 10**9 for v in head), "-10^9 <= node value <= 10^9"
    assert all(head[i] < head[i + 1] for i in range(len(head) - 1)), "values are strictly increasing"
