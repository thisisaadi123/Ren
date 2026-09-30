from ren_gen import distinct
def make(rng, m, n, hit):
    flat = sorted(distinct(rng, m * n, -10**9, 10**9))
    grid = [flat[i * n : (i + 1) * n] for i in range(m)]
    return {"rows": grid, "target": rng.choice(flat) if hit else rng.randint(-10**9, 10**9)}
def small(rng):
    return make(rng, rng.randint(1, 3), rng.randint(1, 3), rng.random() < 0.5)
def build(rng, m, n, hit=1):
    return make(rng, m, n, bool(hit))
