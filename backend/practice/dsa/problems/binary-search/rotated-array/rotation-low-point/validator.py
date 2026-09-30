from ren_check import ints
def validate(readings):
    ints("readings", readings, 1, 100_000, -10**9, 10**9)
    assert len(set(readings)) == len(readings), "values are distinct"
    drops = sum(a > b for a, b in zip(readings, readings[1:]))
    assert drops == 0 or (drops == 1 and readings[-1] < readings[0]), "readings must be a rotated sorted list"
