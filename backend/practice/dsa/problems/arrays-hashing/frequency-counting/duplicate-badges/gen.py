from ren_gen import ints, distinct
def small(rng):
    n = rng.randint(1, 8)
    return {"badges": ints(rng, n, 0, rng.choice([3, 8, 20]))}
def build(rng, n, shape="random"):
    if shape == "distinct":
        return {"badges": distinct(rng, n, -10**9, 10**9)}
    if shape == "far":
        b = distinct(rng, n, -10**9, 10**9)
        b[-1] = b[0]
        return {"badges": b}
    return {"badges": ints(rng, n, -10**9, 10**9) if shape == "wide" else ints(rng, n, 0, 2 * n)}
