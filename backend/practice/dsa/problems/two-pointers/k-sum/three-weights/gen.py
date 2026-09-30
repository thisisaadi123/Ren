from ren_gen import ints
def small(rng):
    return {"weights": ints(rng, rng.randint(3, 7), 1, 9), "target": rng.randint(3, 27)}
def build(rng, n, hi=10**5, hit=True):
    w = ints(rng, n, 1, hi)
    if hit not in (False, "false"):
        i, j, k = rng.sample(range(n), 3)
        target = w[i] + w[j] + w[k]
    else:
        target = rng.randint(1, 3 * hi)
    return {"weights": w, "target": target}
