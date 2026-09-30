def small(rng):
    return build(rng, rng.randint(2, 8), 20)
def build(rng, n, hi=10**9):
    while True:
        vals = sorted(rng.sample(range(-hi, hi + 1), n)) if n <= 2 * hi else sorted(rng.randint(-hi, hi) for _ in range(n))
        i, j = sorted(rng.sample(range(n), 2))
        budget = vals[i] + vals[j]
        seen, count = {}, 0
        for x in vals:
            count += seen.get(budget - x, 0)
            seen[x] = seen.get(x, 0) + 1
        if count == 1:
            return {"prices": vals, "budget": budget}
