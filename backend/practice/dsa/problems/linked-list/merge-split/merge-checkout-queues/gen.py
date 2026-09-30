def small(rng):
    k = rng.randint(0, 5)
    return {"queues": [sorted(rng.randint(-5, 5) for _ in range(rng.randint(0, 4))) for _ in range(k)]}


def build(rng, k, total, span=10**4, shape="random"):
    if shape == "one-long":  # one long queue and many short ones
        sizes = [total - (k - 1)] + [1] * (k - 1)
    elif shape == "empties":
        sizes = [0] * k
        for _ in range(total):
            sizes[rng.randrange(max(1, k // 10))] += 1
    elif shape == "even":
        sizes = [total // k] * k
    else:
        cuts = sorted(rng.randint(0, total) for _ in range(k - 1))
        sizes = [b - a for a, b in zip([0] + cuts, cuts + [total])]
    qs = [sorted(rng.randint(-span, span) for _ in range(s)) for s in sizes]
    rng.shuffle(qs)
    return {"queues": qs}
