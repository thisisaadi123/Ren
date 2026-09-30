from ren_check import ints
def validate(weights):
    ints("weights", weights, 1, 100_000, -1000, 1000)
