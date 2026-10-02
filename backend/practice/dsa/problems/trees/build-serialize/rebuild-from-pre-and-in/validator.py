def validate(preorder, inorder):
    assert isinstance(preorder, list) and isinstance(inorder, list), "lists"
    assert 1 <= len(preorder) == len(inorder) <= 30_000, "1 <= n <= 3 * 10^4, same length"
    assert all(type(v) is int and -10**5 <= v <= 10**5 for v in preorder), "-10^5 <= value <= 10^5"
    assert len(set(preorder)) == len(preorder) and set(preorder) == set(inorder), "distinct values, same set"
    # Check the two walks fit one tree.
    at = {v: i for i, v in enumerate(inorder)}
    pos = 0
    stack = [(0, len(inorder) - 1)]
    while stack:
        lo, hi = stack.pop()
        if lo > hi:
            continue
        m = at[preorder[pos]]
        assert lo <= m <= hi, "the walks don't come from one tree"
        pos += 1
        stack.append((m + 1, hi))
        stack.append((lo, m - 1))
