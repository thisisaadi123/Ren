def check_intervals(xs, name="intervals", lo_n=1, hi_n=100_000, half_open=False, sorted_disjoint=False, touching_ok=True):
    assert isinstance(xs, list) and lo_n <= len(xs) <= hi_n, "%d <= %s.length <= %d" % (lo_n, name, hi_n)
    for p in xs:
        assert isinstance(p, list) and len(p) == 2 and all(type(v) is int for v in p), "each interval is [start, end]"
        assert 0 <= p[0] <= 10**9 and 0 <= p[1] <= 10**9, "0 <= start, end <= 10^9"
        assert p[0] < p[1] if half_open else p[0] <= p[1], "start < end" if half_open else "start <= end"
    if sorted_disjoint:
        for a, b in zip(xs, xs[1:]):
            assert a[1] < b[0] or (touching_ok and a[1] <= b[0]), "%s is sorted and non-overlapping" % name


def validate(lamps, spots):
    check_intervals(lamps, "lamps")
    assert isinstance(spots, list) and 1 <= len(spots) <= 100_000, "1 <= spots.length <= 10^5"
    assert all(type(p) is int and 0 <= p <= 10**9 for p in spots), "0 <= spots[i] <= 10^9"
