def validate(lamps):
    assert isinstance(lamps, list) and 1 <= len(lamps) <= 100_000, "1 to 10^5 lamps"
    for l in lamps:
        assert isinstance(l, list) and len(l) == 2, "each lamp is [position, reach]"
        assert type(l[0]) is int and -10**8 <= l[0] <= 10**8, "-10^8 <= position <= 10^8"
        assert type(l[1]) is int and 0 <= l[1] <= 10**8, "0 <= reach <= 10^8"
