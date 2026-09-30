from ren_check import ints, integer
def validate(stations, extra):
    ints("stations", stations, 2, 2000, 0, 10**8)
    assert all(a < b for a, b in zip(stations, stations[1:])), "stations must be strictly increasing"
    integer("extra", extra, 1, 10**6)
