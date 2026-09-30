def make(rng, n, dup_share):
    rooms = list(range(1, n + 1)); rng.shuffle(rooms)
    k = min(n // 2, int(n * dup_share))
    out = rooms[: n - k] + rooms[: k]
    rng.shuffle(out)
    return {"bookings": out}
def small(rng):
    return make(rng, rng.randint(1, 8), rng.random() / 2)
def build(rng, n, share=0.3):
    return make(rng, n, share)
