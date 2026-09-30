from ren_check import ints
def validate(values):
    ints("values", values, 1, 100_000, -10**4, 10**4)
    assert all(values[i] <= values[i + 1] for i in range(len(values) - 1)), "values must be sorted"
