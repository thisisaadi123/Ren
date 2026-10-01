def validate(readings):
    assert isinstance(readings, list) and 1 <= len(readings) <= 100_000, "1 <= readings.length <= 10^5"
    assert all(type(v) is int and -10**6 <= v <= 10**6 for v in readings), "-10^6 <= readings[i] <= 10^6"
