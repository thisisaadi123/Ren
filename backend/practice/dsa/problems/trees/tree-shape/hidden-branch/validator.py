def parse(level):
    """Level order -> (values, left, right) with child indexes, -1 for none."""
    if not level:
        return [], [], []
    assert level[0] is not None, "the root can't be null"
    val, left, right = [level[0]], [-1], [-1]
    queue, qi, i = [0], 0, 1
    while i < len(level):
        assert qi < len(queue), "malformed level order"
        p = queue[qi]
        qi += 1
        for side in (left, right):
            if i < len(level):
                v = level[i]
                i += 1
                if v is not None:
                    val.append(v)
                    left.append(-1)
                    right.append(-1)
                    side[p] = len(val) - 1
                    queue.append(len(val) - 1)
    return val, left, right


def validate(root, branch):
    a, _, _ = parse(root)
    b, _, _ = parse(branch)
    assert 1 <= len(a) <= 2000, "1 <= root size <= 2000"
    assert 1 <= len(b) <= 1000, "1 <= branch size <= 1000"
    assert all(type(v) is int and -10**4 <= v <= 10**4 for v in a + b), "-10^4 <= node value <= 10^4"
