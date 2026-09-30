def small(rng):
    n = rng.randint(1, 8)
    return {"votes": [rng.randint(0, 2) for _ in range(n)]}
def build(rng, n, share=0.6, options=5):
    winner = rng.randint(0, 10**9)
    votes = [winner if rng.random() < share else rng.randint(0, options) for _ in range(n)]
    rng.shuffle(votes)
    return {"votes": votes}
