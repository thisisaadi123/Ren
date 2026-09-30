def small(rng):
    n = rng.randint(1, 8)
    return build(rng, n, rng.randint(0, 3), 20)
def build(rng, n, k=10, hi=10**9):
    a = sorted(rng.randint(0, hi) for _ in range(n))
    # Shuffle inside disjoint blocks of k + 1, which keeps everyone within k.
    for start in range(0, n, k + 1):
        block = a[start:start + k + 1]
        rng.shuffle(block)
        a[start:start + k + 1] = block
    return {"times": a, "k": k}
