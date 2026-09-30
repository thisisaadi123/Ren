def make(rng, n, lo, hi, tight):
    v = rng.randint(lo, hi)
    k = n // 2 + 1 if tight else rng.randint(n // 2 + 1, n)
    rest = [rng.randint(lo, hi) for _ in range(n - k)]
    rest = [x if x != v else v + 1 for x in rest]
    out = [v] * k + rest
    rng.shuffle(out)
    return out
def small(rng):
    return {"readings": make(rng, rng.randint(1, 9), 0, 4, rng.random() < 0.5)}
def build(rng, n, tight=0):
    return {"readings": make(rng, n, -10**9, 10**9 - 1, bool(tight))}
