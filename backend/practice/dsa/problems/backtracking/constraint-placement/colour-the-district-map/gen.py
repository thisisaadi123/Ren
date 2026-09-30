from ren_gen import graph
def small(rng):
    n = rng.randint(1, 7)
    e = graph(rng, n, rng.randint(0, n * (n - 1) // 2))
    return {"n": n, "borders": e, "m": rng.randint(1, 4)}
def build(rng, n, m=0, density=0.5, shape="random"):
    if not m:
        m = rng.randint(2, 4)
    if shape == "clique":
        k = min(n, m + rng.randint(0, 1))
        nodes = rng.sample(range(n), k)
        e = [[nodes[i], nodes[j]] for i in range(k) for j in range(i + 1, k)]
        e += graph(rng, n, rng.randint(0, n))
        seen, out = set(), []
        for a, b in e:
            key = (min(a, b), max(a, b))
            if key not in seen:
                seen.add(key)
                out.append([a, b] if rng.random() < 0.5 else [b, a])
        rng.shuffle(out)
        return {"n": n, "borders": out, "m": m}
    if shape == "coloured":        # a hidden m-colouring, edges only between different classes
        cls = [rng.randrange(m) for _ in range(n)]
        pairs = [[a, b] for a in range(n) for b in range(a + 1, n) if cls[a] != cls[b]]
        rng.shuffle(pairs)
        k = int(len(pairs) * density)
        out = [p if rng.random() < 0.5 else p[::-1] for p in pairs[:k]]
        return {"n": n, "borders": out, "m": m}
    total = n * (n - 1) // 2
    e = graph(rng, n, int(total * density))
    e = [x if rng.random() < 0.5 else x[::-1] for x in e]
    return {"n": n, "borders": e, "m": m}
