def small(rng):
    return {"floats": rng.sample(range(-10, 11), rng.randint(1, 5))}
def build(rng, n):
    return {"floats": rng.sample(range(-10, 11), n)}
