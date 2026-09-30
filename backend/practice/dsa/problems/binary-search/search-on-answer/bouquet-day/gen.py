from ren_gen import ints
def small(rng):
    b = ints(rng, rng.randint(1, 8), 1, 9)
    return {"bloom": b, "bouquets": rng.randint(1, 4), "size": rng.randint(1, len(b))}
def build(rng, n, size=0, hi=10**9, feasible=1):
    b = ints(rng, n, 1, hi)
    s = size or rng.randint(1, 20)
    most = n // s
    m = rng.randint(1, max(1, most)) if feasible else most + 1
    return {"bloom": b, "bouquets": m, "size": s}
