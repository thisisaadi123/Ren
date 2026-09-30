from ren_gen import tree, _level_order


def avl_like(rng, n, slack):
    # Build a height-balanced shape by splitting sizes; with slack, one deep spot may break it.
    kids = {}
    counter = [0]

    def make(size):
        if size == 0:
            return None
        me = counter[0]
        counter[0] += 1
        kids[me] = [None, None]
        rest = size - 1
        l = rest // 2 + (rng.randint(-1, 1) if rest > 8 else 0)
        l = max(0, min(rest, l))
        kids[me][0] = make(l)
        kids[me][1] = make(rest - l)
        return me

    make(n)
    if slack and n > 3:
        # hang a short chain under the deepest-left node to break balance somewhere low
        cur = 0
        while kids[cur][0] is not None:
            cur = kids[cur][0]
        for _ in range(3):
            i = counter[0]
            counter[0] += 1
            kids[i] = [None, None]
            kids[cur][0] = i
            cur = i
    m = counter[0]
    return _level_order(kids, [rng.randint(-1000, 1000) for _ in range(m)])


def small(rng):
    n = rng.randint(0, 9)
    if rng.random() < 0.4:
        return {"root": avl_like(rng, n, rng.random() < 0.3)}
    return {"root": tree(rng, n, -9, 9, shape=rng.choice(["random", "line", "full"]))}


def build(rng, n, shape="random", slack=False):
    if shape == "balanced":
        return {"root": avl_like(rng, n, slack)}
    return {"root": tree(rng, n, -1000, 1000, shape=shape)}
