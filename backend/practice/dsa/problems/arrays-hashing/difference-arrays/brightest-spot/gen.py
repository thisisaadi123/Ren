def small(rng):
    return {"lamps": [[rng.randint(-5, 5), rng.randint(0, 3)] for _ in range(rng.randint(1, 5))]}
def build(rng, n, spread=10**8, reach=10**6):
    return {"lamps": [[rng.randint(-spread, spread), rng.randint(0, reach)] for _ in range(n)]}
