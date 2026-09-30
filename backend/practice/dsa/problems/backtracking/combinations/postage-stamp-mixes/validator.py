from ren_check import ints, integer
def validate(stamps, target):
    ints("stamps", stamps, 1, 30, 2, 40)
    assert len(set(stamps)) == len(stamps), "stamp values are distinct"
    integer("target", target, 1, 40)
