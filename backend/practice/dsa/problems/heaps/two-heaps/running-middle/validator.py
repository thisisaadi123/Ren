def validate(readings):
    assert isinstance(readings, list) and 1 <= len(readings) <= 10**5, "1 <= readings.length <= 10^5"
    assert all(type(x) is int and -10**9 <= x <= 10**9 for x in readings), "-10^9 <= readings[i] <= 10^9"
