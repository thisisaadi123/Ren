def small(rng):
    return {"slots": [rng.choice([0, 0, 1, 2, -3]) for _ in range(rng.randint(1, 8))]}
def build(rng, n, zeros=0.5):
    return {"slots": [0 if rng.random() < zeros else rng.randint(-10**9, 10**9) for _ in range(n)]}
