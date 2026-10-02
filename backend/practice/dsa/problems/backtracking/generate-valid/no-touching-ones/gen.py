from math import comb


def build(rng, n=20, mode="any"):
    n = rng.randint(max(1, n - 3), n) if n > 4 else rng.randint(1, n)
    while True:
        k = rng.randint(0, (n + 1) // 2 + (1 if mode == "over" else 0))
        if k <= n and comb(n - k + 1, k) <= 10**5:
            return {"n": n, "ones": k}


def small(rng):
    return build(rng, rng.randint(1, 10))
