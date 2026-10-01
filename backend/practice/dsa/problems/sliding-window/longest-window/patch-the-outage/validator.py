def validate(status, k):
    assert isinstance(status, list) and 1 <= len(status) <= 100_000, "1 <= status.length <= 10^5"
    assert all(v in (0, 1) and type(v) is int for v in status), "status[i] is 0 or 1"
    assert type(k) is int and 0 <= k <= len(status), "0 <= k <= status.length"
