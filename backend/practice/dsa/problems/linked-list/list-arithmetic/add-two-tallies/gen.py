def tally(rng, n, nines=False):
    d = [9] * n if nines else [rng.randint(0, 9) for _ in range(n)]
    if d[-1] == 0 and n > 1:
        d[-1] = rng.randint(1, 9)
    return d


def build(rng, n, m=0, shape="random"):
    m = m or n
    if shape == "carry":
        return {"a": tally(rng, n, True), "b": [1]}
    if shape == "nines":
        return {"a": tally(rng, n, True), "b": tally(rng, m, True)}
    return {"a": tally(rng, n), "b": tally(rng, m)}


def small(rng):
    if rng.random() < 0.2:
        return build(rng, rng.randint(1, 5), shape="carry")
    return build(rng, rng.randint(1, 5), rng.randint(1, 5), rng.choice(("random", "random", "nines")))
