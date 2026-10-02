def build(rng, n, q=0, kind="random", deep=0):
    q = q or n
    order = list(range(1, n))
    rng.shuffle(order)
    order = [0] + order
    parent = [-1] * n
    for i in range(1, n):
        if kind == "line":
            p = order[i - 1]
        elif kind == "two-lines":
            p = order[i - 2] if i >= 2 else order[0]
        else:
            p = order[rng.randrange(i)]
        parent[order[i]] = p
    if deep:
        tail = order[-max(1, n // 10):]
        queries = [[rng.choice(tail), rng.choice(tail)] for _ in range(q)]
    else:
        queries = [[rng.randrange(n), rng.randrange(n)] for _ in range(q)]
    return {"parent": parent, "queries": queries}


def small(rng):
    return build(rng, rng.randint(1, 8), rng.randint(1, 6), rng.choice(("random", "line", "two-lines")))
