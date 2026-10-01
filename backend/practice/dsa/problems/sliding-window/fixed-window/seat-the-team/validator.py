def validate(seats):
    assert isinstance(seats, list) and 1 <= len(seats) <= 100_000, "1 <= seats.length <= 10^5"
    assert all(v in (0, 1) and type(v) is int for v in seats), "seats[i] is 0 or 1"
