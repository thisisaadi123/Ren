def validate(root):
    assert isinstance(root, list) and root and root[0] is not None, "the tree has at least one node"
    vals = [v for v in root if v is not None]
    assert 1 <= len(vals) <= 10_000, "1 <= n <= 10^4"
    assert all(type(v) is int and -10**5 <= v <= 10**5 for v in vals), "-10^5 <= node value <= 10^5"
    assert len(set(vals)) == len(vals), "values are distinct"
    # Rebuild and check the search-tree order.
    left, right, queue, qi, i = {}, {}, [0], 0, 1
    while i < len(root):
        assert qi < len(queue), "malformed level order"
        p = queue[qi]
        qi += 1
        for side in (left, right):
            if i < len(root):
                if root[i] is not None:
                    side[p] = i
                    queue.append(i)
                i += 1
    order, stack, node = [], [], 0
    while stack or node is not None:
        while node is not None:
            stack.append(node)
            node = left.get(node)
        node = stack.pop()
        order.append(root[node])
        node = right.get(node)
    assert all(order[k] < order[k + 1] for k in range(len(order) - 1)), "root is a valid binary search tree"
