def rev(rng, d, alpha):
    return "".join(rng.choice(alpha) for _ in range(rng.randint(1, d)))
def release(rng, n, d, alpha):
    parts, size = [], -1
    while True:
        r = rev(rng, d, alpha)
        if parts and size + 1 + len(r) > n:
            break
        parts.append(r[:n])
        size += 1 + len(parts[-1])
    return parts
def pad(rng, r):
    return "0" * rng.randint(0, 50 - len(r)) + r if rng.random() < 0.3 else r
def small(rng):
    alpha = rng.choice(["0012", "01", "0123456789"])
    a = release(rng, rng.randint(1, 12), 3, alpha)
    if rng.random() < 0.5:
        b = release(rng, rng.randint(1, 12), 3, alpha)
    else:
        b = [r if rng.random() < 0.7 else rev(rng, 3, alpha) for r in a]
        b += ["0"] * rng.randint(0, 2)
    return {"a": ".".join(a), "b": ".".join(b)}
def build(rng, n, d=3, alpha="dec", shape="random"):
    alpha = {"dec": "0123456789", "low": "012", "bin": "01"}[alpha]
    if shape == "random":
        return {"a": ".".join(release(rng, n, d, alpha)), "b": ".".join(release(rng, n, d, alpha))}
    parts = [r.lstrip("0") or "0" for r in release(rng, n // 2, d, alpha)]
    a, b = parts[:], []
    budget = n - len(".".join(parts))
    for r in parts:
        q = pad(rng, r)
        if len(q) - len(r) > budget:
            q = r
        budget -= len(q) - len(r)
        b.append(q)
    if shape == "late":
        k = rng.randrange(max(0, len(b) - 3), len(b))
        b[k] = str(int(b[k]) + rng.choice([-1, 1])) if b[k].strip("0") else "1"
        b[k] = b[k].lstrip("-") or "1"
    while len(".".join(b)) + 2 <= n and rng.random() < 0.9:
        b.append("0" * rng.randint(1, 3))
    a, b = ".".join(a), ".".join(b)
    return {"a": a, "b": b} if rng.random() < 0.5 else {"a": b, "b": a}
