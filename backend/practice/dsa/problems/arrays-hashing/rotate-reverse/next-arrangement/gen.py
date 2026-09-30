from ren_gen import ints
def small(rng):
    return {"values": ints(rng, rng.randint(1, 6), 0, 3)}
def build(rng, n, hi=100, shape="random"):
    a = ints(rng, n, 0, hi)
    if shape == "descending":
        a.sort(reverse=True)
    elif shape == "tail":
        k = min(n, rng.randint(2, 50))
        a[n - k:] = sorted(a[n - k:], reverse=True)
    return {"values": a}
