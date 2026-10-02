def build(rng, n=1000, kmax=1000):
    return {"n": rng.randint(1, n), "k": rng.randint(1, kmax)}


def small(rng):
    return build(rng, 12, 15)
