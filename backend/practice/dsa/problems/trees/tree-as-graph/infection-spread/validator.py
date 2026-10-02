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


def check_tree(root):
    val, left, right = parse(root)
    assert 1 <= len(val) <= 10000, "1 <= n <= 10000"
    assert all(type(v) is int and 0 <= v <= 100000 for v in val), "0 <= node value <= 100000"
    assert len(set(val)) == len(val), "values are distinct"
    return val, left, right


def validate(root, start):
    val, _, _ = check_tree(root)
    assert start in val, "start is in the tree"
