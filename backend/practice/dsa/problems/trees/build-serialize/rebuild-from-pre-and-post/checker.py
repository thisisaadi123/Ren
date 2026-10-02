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


def walks(level):
    val, left, right = parse(level)
    pre, post = [], []
    stack = [(0, False)] if val else []
    while stack:
        i, done = stack.pop()
        if done:
            post.append(val[i])
            continue
        pre.append(val[i])
        stack.append((i, True))
        for c in (right[i], left[i]):
            if c >= 0:
                stack.append((c, False))
    return pre, post


def check(args, expected, actual):
    if not isinstance(actual, list) or not actual or actual[0] is None:
        return "the answer must be a non-empty tree"
    try:
        pre, post = walks(actual)
    except AssertionError as e:
        return str(e)
    if pre != args["preorder"]:
        return "the tree's pre-order walk doesn't match preorder"
    if post != args["postorder"]:
        return "the tree's post-order walk doesn't match postorder"
    return True
