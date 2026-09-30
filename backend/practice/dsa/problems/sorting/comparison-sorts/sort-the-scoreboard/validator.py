from ren_check import ints
def validate(scores):
    ints("scores", scores, 1, 100_000, -10**9, 10**9)
