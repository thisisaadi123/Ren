def small(rng):
    return {"volume": round(rng.uniform(-50, 50), 3)}
def build(rng, hi=10**9, shape="random"):
    if shape == "cube":
        r = rng.randint(-int(hi ** (1 / 3)), int(hi ** (1 / 3)))
        return {"volume": float(r ** 3)}
    if shape == "tiny":
        return {"volume": rng.uniform(-1, 1)}
    return {"volume": rng.uniform(-hi, hi)}
