from ren_check import integer
def validate(cans):
    integer("cans", cans, 1, 9 * 10**15)
