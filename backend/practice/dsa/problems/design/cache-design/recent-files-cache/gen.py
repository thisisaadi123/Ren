def calls(rng, capacity, n, ids):
    out = [["RecentFilesCache", capacity]]
    for _ in range(n):
        if rng.random() < 0.5:
            out.append(["open", rng.randint(0, ids)])
        else:
            out.append(["save", rng.randint(0, ids), rng.randint(0, 100_000)])
    return out


def small(rng):
    return {"calls": calls(rng, rng.randint(1, 4), rng.randint(1, 25), rng.randint(1, 8))}


def build(rng, n, capacity=100, ids=300):
    return {"calls": calls(rng, capacity, n, ids)}
