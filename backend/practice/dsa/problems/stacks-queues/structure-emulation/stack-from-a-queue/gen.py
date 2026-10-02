def ops(rng, n, push=55, hi=10**9):
    calls, size = [["QueueStack"]], 0
    for _ in range(n):
        r = rng.randrange(100)
        want = "push" if r < push else rng.choice(("pop", "pop", "top", "empty"))
        if want in ("pop", "top") and size == 0:
            want = "push"
        if want == "push":
            calls.append(["push", rng.randint(1, hi)])
            size += 1
        elif want == "pop":
            calls.append(["pop"])
            size -= 1
        else:
            calls.append([want])
    return calls


def small(rng):
    return {"calls": ops(rng, rng.randint(1, 10), rng.choice((40, 60)), 9)}


def build(rng, n, push=55, hi=10**9):
    return {"calls": ops(rng, n, push, hi)}
