def small(rng):
    return {"head": [rng.randint(0, 6) for _ in range(rng.randint(0, 8))], "pivot": rng.randint(0, 7)}


def build(rng, n, span=10**6, shape="random"):
    head = [rng.randint(-span, span) for _ in range(n)]
    if shape == "all-low":
        return {"head": head, "pivot": span + 1 if span < 10**6 else 10**6}
    if shape == "all-high":
        return {"head": head, "pivot": -span}
    if shape == "zigzag":  # low and high alternate
        head = [(-1 - rng.randint(0, span - 1)) if i % 2 else rng.randint(0, span) for i in range(n)]
        return {"head": head, "pivot": 0}
    return {"head": head, "pivot": rng.randint(-span, span)}
