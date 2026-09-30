def small(rng):
    return {"head": [rng.randint(-3, 3) for _ in range(rng.randint(0, 9))]}


def build(rng, n, shape="random", r=1000):
    if shape == "positive":  # nothing ever cancels
        return {"head": [rng.randint(1, 1000) for _ in range(n)]}
    if shape == "zeros":
        return {"head": [0 if rng.random() < 0.3 else rng.randint(-r, r) for _ in range(n)]}
    if shape == "nested":  # a b c ... -c -b -a blocks: long cascades cancel at the end of each block
        out = []
        while len(out) < n:
            k = min(rng.randint(1, 500), (n - len(out)) // 2)
            if k == 0:
                out.append(rng.randint(1, r))
                continue
            block = [rng.randint(1, r) for _ in range(k)]
            out += block + [-v for v in reversed(block)]
        return {"head": out[:n]}
    if shape == "walk":  # running total wanders near 0, many cancellations of all lengths
        return {"head": [rng.choice((-1, 1)) * rng.randint(1, r) for _ in range(n)]}
    return {"head": [rng.randint(-r, r) for _ in range(n)]}
