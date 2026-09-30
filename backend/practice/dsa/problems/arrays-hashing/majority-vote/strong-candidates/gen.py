def small(rng):
    return {"votes": [rng.randint(-1, 2) for _ in range(rng.randint(1, 9))]}
def build(rng, n, a=0.4, b=0.35, options=50):
    x, y = rng.sample(range(-10**9, 10**9), 2)
    votes = []
    for _ in range(n):
        r = rng.random()
        votes.append(x if r < a else y if r < a + b else rng.randint(0, options))
    rng.shuffle(votes)
    return {"votes": votes}
