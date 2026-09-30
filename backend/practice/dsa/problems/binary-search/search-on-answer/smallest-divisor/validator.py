from ren_check import ints, integer
def validate(loads, threshold):
    ints("loads", loads, 1, 50_000, 1, 10**6)
    integer("threshold", threshold, len(loads), 10**6)
