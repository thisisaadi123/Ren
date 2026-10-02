def build(rng, n=16, k=4, hi=100, fair=1):
    k = min(k, n)
    if fair:
        sizes = [1] * k
        for _ in range(n - k):
            sizes[rng.randrange(k)] += 1
        target = max(sizes) * rng.randint(1, hi) + rng.randint(0, hi)
        target = max(target, max(sizes))
        xs = []
        for sz in sizes:
            cuts = sorted(rng.sample(range(1, target), sz - 1)) if sz > 1 else []
            parts = [b - a for a, b in zip([0] + cuts, cuts + [target])]
            xs += parts
        rng.shuffle(xs)
        if fair == 2 and len(xs) > 1:
            xs[0] += 1
            xs[1] = max(1, xs[1] - 1) if xs[1] > 1 else xs[1] + k - 1
    else:
        xs = [rng.randint(1, hi) for _ in range(n)]
    return {"scores": [min(10**4, x) for x in xs], "k": k}


def small(rng):
    n = rng.randint(1, 8)
    return build(rng, n, rng.randint(1, n), 10, rng.choice((0, 1, 2)))
