from ren_gen import distinct
def small(rng):
    return {"scores": sorted(distinct(rng, rng.randint(1, 6), -8, 8)), "target": rng.randint(-10, 10)}
def build(rng, n, where="random"):
    a = sorted(distinct(rng, n, -10**9 + 1, 10**9 - 1))
    t = {"front": -10**9, "back": 10**9}.get(where, rng.randint(-10**9, 10**9))
    return {"scores": a, "target": t}
