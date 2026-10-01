def validate(customers, moody, minutes):
    n = len(customers)
    assert isinstance(customers, list) and 1 <= n <= 100_000, "1 <= n <= 10^5"
    assert isinstance(moody, list) and len(moody) == n, "customers and moody have the same length"
    assert all(type(v) is int and 0 <= v <= 1000 for v in customers), "0 <= customers[i] <= 1000"
    assert all(v in (0, 1) and type(v) is int for v in moody), "moody[i] is 0 or 1"
    assert type(minutes) is int and 1 <= minutes <= n, "1 <= minutes <= n"
