from ren_gen import matrix
def small(rng):
    n = rng.randint(1, 5)
    return {"photo": matrix(rng, n, n, -9, 9)}
def build(rng, n):
    return {"photo": matrix(rng, n, n, -1000, 1000)}
