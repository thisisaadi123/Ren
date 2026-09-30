from ren_gen import tree


def small(rng):
    n = rng.randint(0, 8)
    return {"root": tree(rng, n, -9, 9, shape=rng.choice(["random", "random", "line", "full"]))}


def build(rng, n, shape="random"):
    if shape == "broom":
        # a long left chain whose last node carries a complete tree: the only leaves are deep
        import collections
        chain = n // 2
        kids = {i: [i + 1, None] for i in range(chain - 1)}
        m = n - chain
        for j in range(m):
            l, r = 2 * j + 1, 2 * j + 2
            kids[chain + j] = [chain + l if l < m else None, chain + r if r < m else None]
        kids[chain - 1] = [chain, None]
        vals = [rng.randint(-1000, 1000) for _ in range(n)]
        out, q = [], collections.deque([0])
        while q:
            i = q.popleft()
            if i is None:
                out.append(None)
                continue
            out.append(vals[i])
            q.extend(kids[i])
        while out and out[-1] is None:
            out.pop()
        return {"root": out}
    return {"root": tree(rng, n, -1000, 1000, shape=shape)}
