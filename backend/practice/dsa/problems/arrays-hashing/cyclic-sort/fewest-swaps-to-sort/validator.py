from ren_check import ints
def validate(order):
    n = len(order)
    ints("order", order, 1, 100_000, 1, n)
    assert len(set(order)) == n, "order must be a permutation of 1 to n"
