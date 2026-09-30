from ren_check import ints, integer
def validate(spots, sensors):
    ints("spots", spots, 2, 100_000, 1, 10**9)
    assert len(set(spots)) == len(spots), "spots are all different"
    integer("sensors", sensors, 2, len(spots))
