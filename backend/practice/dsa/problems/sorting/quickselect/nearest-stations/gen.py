def small(rng):
    pts = [[rng.randint(-3, 3), rng.randint(-3, 3)] for _ in range(rng.randint(1, 8))]
    return {"stations": pts, "k": rng.randint(1, len(pts))}
def build(rng, n, hi=10**4, k=None):
    pts = [[rng.randint(-hi, hi), rng.randint(-hi, hi)] for _ in range(n)]
    return {"stations": pts, "k": k or rng.randint(1, n)}
