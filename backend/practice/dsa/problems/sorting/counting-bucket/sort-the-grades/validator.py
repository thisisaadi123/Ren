from ren_check import ints
def validate(grades):
    ints("grades", grades, 1, 100_000, 0, 100)
