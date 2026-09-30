from ren_check import integer
def validate(n, k):
    integer("n", n, 1, 15)
    integer("k", k, 1, n)
