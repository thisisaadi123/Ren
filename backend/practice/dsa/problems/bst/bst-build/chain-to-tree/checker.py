def parse(level):
    """Level order -> (values, left, right) with children as indexes, or None if malformed."""
    if not isinstance(level, list) or not level or level[0] is None:
        return None
    val, left, right = [level[0]], [-1], [-1]
    queue, qi, i = [0], 0, 1
    while i < len(level):
        if qi >= len(queue):
            return None
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


def check_balanced(values, actual):
    tree = parse(actual)
    if tree is None:
        return "the answer must be a non-empty tree"
    val, left, right = tree
    order, stack, node = [], [], 0
    while stack or node != -1:
        while node != -1:
            stack.append(node)
            node = left[node]
        node = stack.pop()
        order.append(val[node])
        node = right[node]
    if order != values:
        return "reading the tree in order doesn't give the values in sorted order, so it isn't a search tree of exactly these values"
    height = [0] * len(val)
    for x in range(len(val) - 1, -1, -1):
        hl = height[left[x]] if left[x] != -1 else 0
        hr = height[right[x]] if right[x] != -1 else 0
        if abs(hl - hr) > 1:
            return "the subtrees under %s differ in height by %d" % (val[x], abs(hl - hr))
        height[x] = 1 + max(hl, hr)
    return True


def check(args, expected, actual):
    head = args["head"]
    return check_balanced(head if isinstance(head, list) else head["values"], actual)
