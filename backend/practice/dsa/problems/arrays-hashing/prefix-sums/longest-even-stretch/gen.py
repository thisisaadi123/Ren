from ren_gen import ints
def small(rng):
    return {"bits": ints(rng, rng.randint(1, 10), 0, 1)}
def build(rng, n, bias=50):
    return {"bits": [1 if rng.randrange(100) < bias else 0 for _ in range(n)]}
