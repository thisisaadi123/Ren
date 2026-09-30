from ren_check import matrix, integer
def validate(stations, k):
    matrix("stations", stations, 1, 100_000, 2, 2, -10**4, 10**4)
    integer("k", k, 1, len(stations))
