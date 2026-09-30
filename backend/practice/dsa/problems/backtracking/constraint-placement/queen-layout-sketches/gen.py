def solution(rng, n):
    # a random full layout, found by randomised search (None if n has none)
    cols = list(range(n))
    pos = []
    def go(r):
        if r == n:
            return True
        order = cols[:]
        rng.shuffle(order)
        for c in order:
            if all(c != pc and abs(c - pc) != r - pr for pr, pc in enumerate(pos)):
                pos.append(c)
                if go(r + 1):
                    return True
                pos.pop()
        return False
    return pos if go(0) else None
def make(rng, n, k, shape):
    if shape == "random":
        cells = [[r, c] for r in range(n) for c in range(n)]
        return {"n": n, "fixed": rng.sample(cells, min(k, n))}
    sol = solution(rng, n)
    if sol is None:
        return {"n": n, "fixed": []}
    rows = rng.sample(range(n), min(k, n))
    fixed = [[r, sol[r]] for r in rows]
    if shape == "clash" and len(fixed) >= 2:
        r0, c0 = fixed[0]
        fixed[1] = [fixed[1][0], c0]
    return {"n": n, "fixed": fixed}
def small(rng):
    n = rng.randint(1, 6)
    return make(rng, n, rng.randint(0, 2), rng.choice(["random", "sol", "sol"]))
def build(rng, n, k=1, shape="sol"):
    return make(rng, n, k, shape)
