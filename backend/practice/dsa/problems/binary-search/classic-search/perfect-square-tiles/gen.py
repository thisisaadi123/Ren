def small(rng):
    return {"tiles": rng.randint(1, 200)}
def build(rng, hi, shape="random"):
    r = rng.randint(1, int(hi ** 0.5))
    if shape == "square":
        return {"tiles": r * r}
    if shape == "near":
        return {"tiles": max(1, r * r + rng.choice([-1, 1]))}
    return {"tiles": rng.randint(1, hi)}
