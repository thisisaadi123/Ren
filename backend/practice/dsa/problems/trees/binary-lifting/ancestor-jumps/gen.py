def build(rng, n, q=0, kind="random", far=0):
    q = q or n
    order = list(range(1, n))
    rng.shuffle(order)
    order = [0] + order
    parent = [-1] * n
    for i in range(1, n):
        if kind == "line":
            p = order[i - 1]
        elif kind == "broom":
            p = order[i - 1] if i < n // 2 else order[rng.randrange(max(1, n // 2))]
        else:
            p = order[rng.randrange(i)]
        parent[order[i]] = p
    depth = [0] * n
    for i in range(1, n):
        depth[order[i]] = depth[parent[order[i]]] + 1
    queries = []
    for _ in range(q):
        v = rng.randrange(n)
        if far:
            k = rng.randint(max(1, depth[v] - 2), min(n, depth[v] + 2))
        else:
            k = rng.randint(1, n)
        queries.append([v, k])
    return {"parent": parent, "queries": queries}


def small(rng):
    n = rng.randint(1, 8)
    return build(rng, n, rng.randint(1, 6), rng.choice(("random", "line")), rng.choice((0, 1)))
