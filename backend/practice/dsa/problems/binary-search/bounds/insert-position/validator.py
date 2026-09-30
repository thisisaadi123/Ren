from ren_check import ints, integer
def validate(scores, target):
    ints("scores", scores, 1, 100_000, -10**9, 10**9)
    assert all(a < b for a, b in zip(scores, scores[1:])), "scores must be strictly increasing"
    integer("target", target, -10**9, 10**9)
