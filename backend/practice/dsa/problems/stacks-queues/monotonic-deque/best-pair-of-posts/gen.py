def build(rng, n, gap=10, k=0, hi=10**8, shape="random"):
    xs, x = [], -10**8
    for _ in range(n):
        x += rng.randint(1, gap)
        xs.append(x)
    if shape == "falling":
        ys = sorted((rng.randint(-hi, hi) for _ in range(n)), reverse=True)
    else:
        ys = [rng.randint(-hi, hi) for _ in range(n)]
    min_gap = min(xs[i + 1] - xs[i] for i in range(n - 1))
    k = max(k or rng.randint(1, gap * 5), min_gap)
    return {"posts": [[a, b] for a, b in zip(xs, ys)], "k": min(k, 2 * 10**8)}


def small(rng):
    return build(rng, rng.randint(2, 7), rng.choice((1, 3, 6)), 0, rng.choice((5, 50)))
