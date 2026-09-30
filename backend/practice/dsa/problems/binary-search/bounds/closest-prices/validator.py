from ren_check import ints, integer
def validate(prices, k, x):
    ints("prices", prices, 1, 100_000, -10**9, 10**9)
    assert all(a <= b for a, b in zip(prices, prices[1:])), "prices must be sorted"
    integer("k", k, 1, len(prices))
    integer("x", x, -10**9, 10**9)
