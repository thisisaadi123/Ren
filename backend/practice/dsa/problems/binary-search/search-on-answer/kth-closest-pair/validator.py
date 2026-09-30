from ren_check import ints, integer
def validate(heights, k):
    n = len(heights)
    ints("heights", heights, 2, 20_000, 0, 10**6)
    integer("k", k, 1, n * (n - 1) // 2)
