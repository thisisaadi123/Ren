from ren_check import ints, integer
def validate(times, target):
    ints("times", times, 0, 100_000, -10**9, 10**9)
    assert all(a <= b for a, b in zip(times, times[1:])), "times must be non-decreasing"
    integer("target", target, -10**9, 10**9)
