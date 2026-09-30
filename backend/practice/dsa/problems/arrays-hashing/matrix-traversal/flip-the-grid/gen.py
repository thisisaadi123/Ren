from ren_gen import matrix
def small(rng):
    return {"grid": matrix(rng, rng.randint(1, 4), rng.randint(1, 4), -9, 9)}
def build(rng, m, n):
    return {"grid": matrix(rng, m, n, -10**9, 10**9)}
