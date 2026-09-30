def small(rng):
    plays = [rng.randint(0, 4) for _ in range(rng.randint(1, 9))]
    return {"plays": plays, "k": rng.randint(1, len(set(plays)))}
def build(rng, n, songs=100, k=None):
    ids = rng.sample(range(0, 10**9), songs)
    weights = [rng.random() ** 3 for _ in ids]
    plays = rng.choices(ids, weights, k=n)
    distinct = len(set(plays))
    return {"plays": plays, "k": min(k or distinct // 2 or 1, distinct)}
