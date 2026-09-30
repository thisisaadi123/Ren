def small(rng):
    n = rng.randint(1, 9)
    hi = rng.choice([3, 6, 12])
    return {"cards": [rng.randint(1, hi) for _ in range(n)], "target": rng.randint(1, 15)}
def build(rng, n, hi=10, target=0, shape="random"):
    if shape == "ones":
        cards = [1] * n
    elif shape == "two":
        cards = [rng.choice([1, 2]) for _ in range(n)]
    else:
        cards = [rng.randint(1, hi) for _ in range(n)]
    return {"cards": cards, "target": target if target else rng.randint(1, 30)}
