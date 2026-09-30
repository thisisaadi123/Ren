from ren_check import ints
def validate(codes):
    ints("codes", codes, 1, 100_000, -10**4, 10**4)
    assert all(codes[i] <= codes[i + 1] for i in range(len(codes) - 1)), "codes must be sorted"
