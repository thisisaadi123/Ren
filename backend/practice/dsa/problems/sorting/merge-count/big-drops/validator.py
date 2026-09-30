from ren_check import ints
def validate(prices):
    ints("prices", prices, 1, 50_000, -2**31, 2**31 - 1)
