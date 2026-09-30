from ren_check import ints
def validate(strength):
    ints("strength", strength, 1, 10**5, 1, 10**6)
