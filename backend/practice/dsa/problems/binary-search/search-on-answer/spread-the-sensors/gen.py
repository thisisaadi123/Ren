from ren_gen import distinct
def small(rng):
    s = distinct(rng, rng.randint(2, 7), 1, 20)
    return {"spots": s, "sensors": rng.randint(2, len(s))}
def build(rng, n, sensors=0, hi=10**9):
    s = distinct(rng, n, 1, hi)
    return {"spots": s, "sensors": sensors or rng.randint(2, n)}
