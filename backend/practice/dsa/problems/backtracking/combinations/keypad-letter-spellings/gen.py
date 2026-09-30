from ren_gen import word
def small(rng):
    return {"digits": word(rng, rng.randint(0, 3), "23456789")}
def build(rng, n, alpha="23456789"):
    return {"digits": word(rng, n, str(alpha))}
