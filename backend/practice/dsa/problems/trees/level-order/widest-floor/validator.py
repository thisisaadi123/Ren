from ren_check import tree


def validate(root):
    tree("root", root, 10**5, -1000, 1000, min_nodes=1)
    # the width of every floor, with exact integers
    import collections
    it = iter(root[1:])
    level, best = [0], 1
    while level:
        best = max(best, level[-1] - level[0] + 1)
        nxt = []
        for p in level:
            p -= level[0]
            for side in (0, 1):
                v = next(it, None)
                if v is not None:
                    nxt.append(2 * p + side)
        level = nxt
    assert best <= 10**18, "the answer is at most 10^18"
