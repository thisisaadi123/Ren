def validate(readings, limit):
    assert isinstance(readings, list) and 1 <= len(readings) <= 100_000, "1 <= readings.length <= 10^5"
    assert all(type(v) is int and 1 <= v <= 10**9 for v in readings), "1 <= readings[i] <= 10^9"
    assert type(limit) is int and 0 <= limit <= 10**9, "0 <= limit <= 10^9"
