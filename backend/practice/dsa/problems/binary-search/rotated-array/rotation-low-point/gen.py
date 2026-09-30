from ren_gen import distinct
def rotated(rng, n, lo, hi, k=None):
    a = sorted(distinct(rng, n, lo, hi))
    k = rng.randrange(n) if k is None else k % n
    return a[k:] + a[:k]

def small(rng):
    return {"readings": rotated(rng, rng.randint(1, 8), -9, 9)}
def build(rng, n, k=-1):
    return {"readings": rotated(rng, n, -10**9, 10**9, None if k < 0 else k)}
