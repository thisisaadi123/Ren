def small(rng):
    return {"head": [rng.randint(1, 4) for _ in range(rng.randint(0, 8))], "bad": rng.randint(1, 4)}


def build(rng, n, shape="random", colours=50):
    bad = rng.randint(1, colours)
    good = [c for c in range(1, 51) if c != bad]
    if shape == "tail-bad":  # good beads first, then a long faulty run
        h = n // 2
        return {"head": [rng.choice(good) for _ in range(h)] + [bad] * (n - h), "bad": bad}
    if shape == "all-bad":
        return {"head": [bad] * n, "bad": bad}
    if shape == "alternate":
        return {"head": [bad if i % 2 == 0 else rng.choice(good) for i in range(n)], "bad": bad}
    return {"head": [rng.randint(1, colours) for _ in range(n)], "bad": bad}
