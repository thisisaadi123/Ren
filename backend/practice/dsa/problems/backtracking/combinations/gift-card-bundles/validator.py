from ren_check import ints, integer
def validate(cards, target):
    ints("cards", cards, 1, 40, 1, 50)
    integer("target", target, 1, 30)
