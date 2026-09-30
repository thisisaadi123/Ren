from ren_check import ints
def validate(days):
    ints("days", days, 0, 100_000, -10**9, 10**9)
