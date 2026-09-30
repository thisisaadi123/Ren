def make(rng, n, missing=None):
    m = rng.randint(0, n) if missing is None else missing
    s = [i for i in range(n + 1) if i != m]
    rng.shuffle(s)
    return {"seats": s}
def small(rng):
    return make(rng, rng.randint(1, 8))
def build(rng, n, where="random"):
    return make(rng, n, {"first": 0, "last": n}.get(where))
