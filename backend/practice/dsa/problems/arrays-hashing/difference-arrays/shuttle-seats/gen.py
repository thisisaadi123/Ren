def make(rng, m, road, cap):
    trips = []
    for _ in range(m):
        a = rng.randrange(road); b = rng.randint(a + 1, min(road, a + 1 + rng.randint(0, road)))
        trips.append([rng.randint(1, 100), a, b])
    if cap == 0:  # pick a capacity right at the busiest moment, give or take one
        change = [0] * (road + 1)
        for p, a, b in trips:
            change[a] += p; change[b] -= p
        best = run = 0
        for c in change:
            run += c; best = max(best, run)
        cap = max(1, best + rng.choice([-1, 0]))
    return {"capacity": cap, "trips": trips}
def small(rng):
    return make(rng, rng.randint(1, 4), rng.randint(1, 6), rng.choice([0, rng.randint(1, 200)]))
def build(rng, m, road, cap=0):
    return make(rng, m, road, cap)
