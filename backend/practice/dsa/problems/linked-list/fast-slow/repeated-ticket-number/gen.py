def make(rng, n, copies):
    rep = rng.randint(1, n)
    copies = max(2, min(copies, n + 1))
    others = [v for v in range(1, n + 1) if v != rep]
    rng.shuffle(others)
    arr = [rep] * copies + others[: n + 1 - copies]
    rng.shuffle(arr)
    return arr


def small(rng):
    n = rng.randint(1, 8)
    return {"tickets": make(rng, n, rng.choice([2, 2, 3, n + 1]))}


def build(rng, n, copies=2, shape="random"):
    if shape == "chain":  # 0 -> 1 -> 2 -> ... long tail, then a loop back near the start
        arr = list(range(1, n + 1)) + [0]
        rep = rng.randint(1, max(1, n // 50))
        arr[n] = rep  # value rep appears at index rep-1 and at index n
        return {"tickets": arr}
    if copies == -1:
        copies = rng.randint(2, n + 1)
    return {"tickets": make(rng, n, copies)}
