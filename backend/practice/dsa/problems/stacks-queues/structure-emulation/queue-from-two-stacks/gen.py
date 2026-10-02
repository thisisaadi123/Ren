def ops(rng, n, push=55, hi=10**9, shape="random"):
    calls, size = [["TwoStackQueue"]], 0
    for i in range(n):
        if shape == "fill-drain":
            want = "push" if i < n // 2 else "pop"
        elif shape == "zigzag":
            # Alternate long push runs with a single pop, so a naive queue keeps re-moving everything.
            want = "pop" if i % 50 == 49 else "push"
        else:
            r = rng.randrange(100)
            want = "push" if r < push else rng.choice(("pop", "pop", "peek", "empty"))
        if want in ("pop", "peek") and size == 0:
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


def build(rng, n, push=55, hi=10**9, shape="random"):
    return {"calls": ops(rng, n, push, hi, shape)}
