def small(rng):
    return {"readings": [rng.randint(0, 3) for _ in range(rng.randint(1, 8))]}
def build(rng, n, distinct=5):
    pool = [rng.randint(0, 10**9) for _ in range(distinct)]
    return {"readings": [rng.choice(pool) for _ in range(n)]}
