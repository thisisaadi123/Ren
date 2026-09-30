from ren_check import ints
def validate(panels):
    ints("panels", panels, 1, 10**5, 1, 10**9)
