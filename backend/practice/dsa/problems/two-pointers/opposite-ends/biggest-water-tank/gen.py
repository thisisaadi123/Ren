from ren_gen import ints
def small(rng):
    return {"posts": ints(rng, rng.randint(2, 8), 0, 9)}
def build(rng, n, hi=10**9, shape="random"):
    a = ints(rng, n, 0, hi)
    if shape == "increasing":
        a.sort()
    elif shape == "middle":
        a = [1] * n
        a[n // 2 - 1] = a[n // 2] = hi
    return {"posts": a}
