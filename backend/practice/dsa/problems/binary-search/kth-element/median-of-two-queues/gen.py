from ren_gen import ints
def two(rng, n, m, spread):
    return sorted(ints(rng, n, -spread, spread)), sorted(ints(rng, m, -spread, spread))

def small(rng):
    n, m = rng.randint(0, 5), rng.randint(0, 5)
    if n + m == 0:
        n = 1
    a, b = two(rng, n, m, 6)
    return {"a": a, "b": b}
def build(rng, n, m, spread=10**6, shape="random"):
    a, b = two(rng, n, m, spread)
    if shape == "apart":
        a = [x - 2 * 10**6 if x - 2 * 10**6 >= -10**6 else -10**6 for x in a]
    return {"a": a, "b": b}
