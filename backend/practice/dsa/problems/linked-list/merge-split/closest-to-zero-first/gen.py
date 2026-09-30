def small(rng):
    return {"head": [rng.randint(-4, 4) for _ in range(rng.randint(0, 9))]}


def build(rng, n, span=10**9, shape="random"):
    if shape == "descending":  # farthest first: worst case for insertion
        vals = sorted((rng.randint(0, span) for _ in range(n)), reverse=True)
        return {"head": [v if rng.random() < 0.5 else -v for v in vals]}
    if shape == "pairs":  # lots of +x / -x ties
        return {"head": [rng.choice((-1, 1)) * rng.randint(0, span) for _ in range(n)]}
    return {"head": [rng.randint(-span, span) for _ in range(n)]}
