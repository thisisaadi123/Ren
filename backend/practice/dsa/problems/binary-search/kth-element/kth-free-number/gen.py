from ren_gen import distinct
def small(rng):
    return {"taken": sorted(distinct(rng, rng.randint(1, 5), 1, 12)), "k": rng.randint(1, 10)}
def build(rng, n, hi=10**9, k=0):
    return {"taken": sorted(distinct(rng, n, 1, max(hi, n))), "k": k or rng.randint(1, 10**9)}
