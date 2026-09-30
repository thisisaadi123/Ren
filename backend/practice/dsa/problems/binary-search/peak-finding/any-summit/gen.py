def make(rng, n, shape):
    if shape == "up":
        return list(range(n))
    if shape == "down":
        return list(range(n, 0, -1))
    a = [rng.randint(-50, 50)]
    for _ in range(n - 1):
        step = rng.randint(1, 3) * rng.choice([1, -1])
        a.append(a[-1] + step)
    return a
def small(rng):
    return {"heights": make(rng, rng.randint(1, 8), rng.choice(["up", "down", "wiggle"]))}
def build(rng, n, shape="wiggle"):
    return {"heights": make(rng, n, shape)}
