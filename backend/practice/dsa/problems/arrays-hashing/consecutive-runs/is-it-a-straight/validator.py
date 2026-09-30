from ren_check import ints
def validate(cards):
    ints("cards", cards, 1, 100_000, -10**9, 10**9)
