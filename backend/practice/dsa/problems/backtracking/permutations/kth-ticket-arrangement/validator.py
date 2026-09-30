import math
from ren_check import integer
def validate(n, k):
    integer("n", n, 1, 18)
    integer("k", k, 1, math.factorial(n))
