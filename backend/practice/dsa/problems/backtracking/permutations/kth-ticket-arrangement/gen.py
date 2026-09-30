import math
def small(rng):
    n = rng.randint(1, 7)
    return {"n": n, "k": rng.randint(1, math.factorial(n))}
def build(rng, n, shape="random"):
    f = math.factorial(n)
    if shape == "last":
        k = f
    elif shape == "high":
        k = f - rng.randint(0, min(f - 1, 10**6))
    elif shape == "mid":
        k = f // 2 + rng.randint(0, 1)
        k = min(max(k, 1), f)
    else:
        k = rng.randint(1, f)
    return {"n": n, "k": k}
