def small(rng):
    return build(rng, rng.randint(2, 8))
def build(rng, n):
    labels = list(range(1, n + 1))
    missing = rng.randint(1, n)
    dup = rng.choice([x for x in range(1, n + 1) if x != missing])
    labels[labels.index(missing)] = dup
    rng.shuffle(labels)
    return {"labels": labels}
