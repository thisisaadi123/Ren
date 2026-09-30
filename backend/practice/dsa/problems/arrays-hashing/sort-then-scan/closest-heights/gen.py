from ren_gen import ints, distinct
def small(rng):
    return {"heights": ints(rng, rng.randint(2, 8), 0, 30)}
def build(rng, n, shape="random"):
    if shape == "distinct":
        return {"heights": distinct(rng, n, 0, 10**9)}
    return {"heights": ints(rng, n, 0, 10**9)}
