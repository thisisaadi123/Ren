def small(rng):
    return {"x": rng.randint(0, 200)}
def build(rng, hi, shape="random"):
    if shape == "square":
        r = rng.randint(0, int(hi ** 0.5)); return {"x": r * r}
    if shape == "below-square":
        r = rng.randint(1, int(hi ** 0.5)); return {"x": r * r - 1}
    return {"x": rng.randint(0, hi)}
