from ren_check import ints, integer
def validate(taken, k):
    ints("taken", taken, 1, 100_000, 1, 10**9)
    assert all(a < b for a, b in zip(taken, taken[1:])), "taken must be strictly increasing"
    integer("k", k, 1, 10**9)
