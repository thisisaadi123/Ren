from ren_check import ints, integer
def validate(cells, blank):
    ints("cells", cells, 1, 100_000, 0, 100)
    integer("blank", blank, 0, 100)
