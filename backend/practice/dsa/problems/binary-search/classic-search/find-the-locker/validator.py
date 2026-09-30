from ren_check import ints, integer
def validate(lockers, target):
    ints("lockers", lockers, 1, 100_000, -10**9, 10**9)
    assert all(a < b for a, b in zip(lockers, lockers[1:])), "lockers must be strictly increasing"
    integer("target", target, -10**9, 10**9)
