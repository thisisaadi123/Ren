def small(rng):
    head = sorted(rng.randint(-5, 5) for _ in range(rng.randint(0, 7)))
    return {"head": head, "value": rng.randint(-6, 6)}


def build(rng, n, where="random", span=10**6):
    head = sorted(rng.randint(-span, span) for _ in range(n))
    if where == "front":
        value = -10**6
        head = [max(v, -10**6 + 1) for v in head]
    elif where == "back":
        value = 10**6
    else:
        value = rng.randint(-span, span)
    return {"head": head, "value": value}
