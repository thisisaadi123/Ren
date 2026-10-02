def build(rng, n, k=0, add=50):
    k = k or rng.randint(1, 1000)
    calls = [["RingBuffer", k]]
    for _ in range(n):
        r = rng.randrange(100)
        if r < add:
            calls.append(["enqueue", rng.randint(0, 1000)])
        else:
            calls.append([rng.choice(("dequeue", "dequeue", "front", "rear", "isEmpty", "isFull"))])
    return {"calls": calls}


def small(rng):
    return build(rng, rng.randint(1, 12), rng.randint(1, 3), rng.choice((40, 60, 75)))
