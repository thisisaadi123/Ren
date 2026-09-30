from ren_check import ints
def validate(badges):
    ints("badges", badges, 1, 100_000, -10**9, 10**9)
