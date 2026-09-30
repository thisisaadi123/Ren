def small(rng):
    n = rng.randint(0, 7)
    at = rng.randint(-1, n - 1) if n and rng.random() < 0.6 else -1
    return {"head": {"values": [rng.randint(-3, 3) for _ in range(n)], "cycle_at": at}}


def build(rng, n, loop="random", span=10**5):
    vals = [rng.randint(-span, span) for _ in range(n)]
    at = {"none": -1, "head": 0, "tail": n - 1, "random": rng.randint(-1, n - 1)}.get(loop)
    if at is None:
        at = int(loop)
    return {"head": {"values": vals, "cycle_at": at}}
