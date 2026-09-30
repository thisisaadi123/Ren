from ren_check import integer
def validate(tiles):
    integer("tiles", tiles, 1, 9 * 10**15)
