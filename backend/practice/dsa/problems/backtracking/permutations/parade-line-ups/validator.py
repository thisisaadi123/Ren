from ren_check import ints
def validate(floats):
    ints("floats", floats, 1, 7, -10, 10)
    assert len(set(floats)) == len(floats), "floats are distinct"
