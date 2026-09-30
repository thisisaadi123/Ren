from ren_check import integer
def validate(capacity, trips):
    integer("capacity", capacity, 1, 10**7)
    assert isinstance(trips, list) and 1 <= len(trips) <= 100_000, "1 to 10^5 trips"
    for t in trips:
        assert isinstance(t, list) and len(t) == 3, "each trip is [passengers, from, to]"
        p, a, b = t
        assert type(p) is int and 1 <= p <= 100, "1 <= passengers <= 100"
        assert type(a) is int and type(b) is int and 0 <= a < b <= 10**5, "0 <= from < to <= 10^5"
