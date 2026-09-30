from ren_check import ints, integer
def validate(shelf, target):
    ints("shelf", shelf, 1, 100_000, -10**4, 10**4)
    drops = sum(a > b for a, b in zip(shelf, shelf[1:]))
    assert drops == 0 or (drops == 1 and shelf[-1] <= shelf[0]), "shelf must be a rotated non-decreasing list"
    integer("target", target, -10**4, 10**4)
