def small(rng):
    return build(rng, rng.randint(1, 6), 5)
def build(rng, n, hi=10**6):
    heights = [rng.randint(1, hi) for _ in range(n)]
    people = [[h, sum(1 for g in heights[:i] if g >= h)] for i, h in enumerate(heights)]
    rng.shuffle(people)
    return {"people": people}
