def validate(depot, position, speed):
    assert type(depot) is int and 1 <= depot <= 10**6, "1 <= depot <= 10^6"
    assert isinstance(position, list) and 1 <= len(position) <= 100_000, "1 <= n <= 10^5"
    assert isinstance(speed, list) and len(speed) == len(position), "position and speed have the same length"
    assert all(type(v) is int and 0 <= v < depot for v in position), "0 <= position[i] < depot"
    assert len(set(position)) == len(position), "positions are distinct"
    assert all(type(v) is int and 1 <= v <= 10**6 for v in speed), "1 <= speed[i] <= 10^6"
