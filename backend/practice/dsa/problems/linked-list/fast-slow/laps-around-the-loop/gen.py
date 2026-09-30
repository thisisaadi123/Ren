def small(rng):
    n = rng.randint(1, 6)
    at = rng.randint(-1, n - 1)
    return {"head": {"values": [rng.randint(0, 9) for _ in range(n)], "cycle_at": at},
            "steps": [rng.randint(0, 14) for _ in range(rng.randint(1, 4))]}


def build(rng, n, q, loop="random", big=10**15, span=10**9):
    vals = [rng.randint(0, span) for _ in range(n)]
    at = {"none": -1, "head": 0, "tail": n - 1, "random": rng.randint(-1, n - 1)}.get(loop)
    if at is None:
        at = int(loop)
    steps = []
    for _ in range(q):
        r = rng.random()
        if r < 0.3:
            steps.append(rng.randint(0, 2 * n))
        elif r < 0.4:
            steps.append(big - rng.randint(0, 5))
        else:
            steps.append(rng.randint(0, big))
    return {"head": {"values": vals, "cycle_at": at}, "steps": steps}
