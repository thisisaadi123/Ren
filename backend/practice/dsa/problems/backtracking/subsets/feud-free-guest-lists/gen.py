def small(rng):
    n = rng.randint(1, 7)
    k = rng.randint(1, 3)
    return {"ages": [rng.randint(1, 8) for _ in range(n)], "k": k}
def build(rng, n, k=0, shape="random", span=0):
    if not k:
        k = rng.randint(1, 5)
    if shape == "chain":          # ages step by k, so neighbours clash
        base = rng.randint(1, 1000 - k * n) if 1000 - k * n > 1 else 1
        a = [base + k * i for i in range(n)]
        rng.shuffle(a)
        return {"ages": a, "k": k}
    if shape == "free":           # values from alternating blocks of k: no two differ by exactly k
        pool = [x for x in range(1, 1001) if ((x - 1) // k) % 2 == 0]
        return {"ages": [rng.choice(pool) for _ in range(n)], "k": k}
    if shape == "pairs":          # repeated ages on both sides of a clash
        x = rng.randint(1, 1000 - k)
        a = [rng.choice([x, x + k]) for _ in range(n)]
        return {"ages": a, "k": k}
    hi = span if span else rng.randint(k + 1, 4 * k + 6)
    return {"ages": [rng.randint(1, min(1000, hi)) for _ in range(n)], "k": k}
