from ren_gen import distinct
def rotated(rng, n, lo, hi, k=None):
    a = sorted(distinct(rng, n, lo, hi))
    k = rng.randrange(n) if k is None else k % n
    return a[k:] + a[:k]

def small(rng):
    a = rotated(rng, rng.randint(1, 8), -9, 9)
    return {"playlist": a, "target": rng.choice(a) if rng.random() < 0.6 else rng.randint(-10, 10)}
def build(rng, n, k=-1, hit=1):
    a = rotated(rng, n, -10**9, 10**9, None if k < 0 else k)
    return {"playlist": a, "target": rng.choice(a) if hit else rng.randint(-10**9, 10**9)}
