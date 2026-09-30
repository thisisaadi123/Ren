def small(rng):
    n = rng.randint(1, 6)
    start = rng.randint(-3, 3)
    cards = list(range(start, start + n))
    if rng.random() < 0.5:
        cards[rng.randrange(n)] += rng.choice([-1, 1, 2])
    rng.shuffle(cards)
    return {"cards": cards}
def build(rng, n, broken="none"):
    start = rng.randint(-10**9, 10**9 - n)
    cards = list(range(start, start + n))
    if broken == "gap":
        cards[-1] += 1
    elif broken == "dup":
        cards[rng.randrange(1, n)] = cards[0]
    rng.shuffle(cards)
    return {"cards": cards}
