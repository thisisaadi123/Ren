from ren_gen import ints
def small(rng):
    return {"weights": ints(rng, rng.randint(1, 7), -3, 3)}
def build(rng, n, shape="random"):
    w = ints(rng, n, -1000, 1000)
    if shape == "balanced":  # force a balance point near the end
        i = rng.randrange(n // 2, n)
        diff = sum(w[:i]) - sum(w[i + 1:])
        j = n - 1 if i != n - 1 else 0
        while diff and j != i:
            step = max(-1000 - w[j], min(1000 - w[j], diff if j > i else -diff))
            w[j] += step
            diff -= step if j > i else -step
            j -= 1
            if j < 0:
                break
    return {"weights": w}
