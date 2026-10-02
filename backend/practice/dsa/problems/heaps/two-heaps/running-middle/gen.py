def build(rng, n, hi=10**9, order="random"):
    xs = [rng.randint(-hi, hi) for _ in range(n)]
    if order == "up":
        xs.sort()
    elif order == "down":
        xs.sort(reverse=True)
    return {"readings": xs}


def small(rng):
    return build(rng, rng.randint(1, 8), rng.choice((3, 10, 100)))
