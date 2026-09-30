from ren_gen import matrix
def small(rng):
    return {"grid": matrix(rng, rng.randint(1, 5), rng.randint(1, 5), -9, 9)}
def build(rng, m, n):
    return {"grid": matrix(rng, m, n, -1000, 1000)}
