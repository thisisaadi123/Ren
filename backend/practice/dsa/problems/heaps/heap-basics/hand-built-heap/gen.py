def build(rng, items, n, hi=10**9, pops=30):
    out = [["TaskHeap", [rng.randint(0, hi) for _ in range(items)]]]
    for _ in range(n):
        r = rng.randrange(100)
        if r < pops:
            out.append(["pop"])
        elif r < pops + 10:
            out.append(["peek"])
        elif r < pops + 15:
            out.append(["size"])
        else:
            out.append(["push", rng.randint(0, hi)])
    return {"calls": out}


def small(rng):
    return build(rng, rng.randint(0, 4), rng.randint(1, 15), rng.choice((3, 20)), rng.choice((30, 60)))
