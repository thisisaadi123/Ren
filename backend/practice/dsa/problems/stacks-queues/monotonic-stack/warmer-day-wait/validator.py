from ren_check import ints
def validate(temps):
    ints("temps", temps, 1, 10**5, -100, 100)
