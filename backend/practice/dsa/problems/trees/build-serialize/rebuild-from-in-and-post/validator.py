def validate(inorder, postorder):
    assert isinstance(postorder, list) and isinstance(inorder, list), "lists"
    assert 1 <= len(postorder) == len(inorder) <= 30_000, "1 <= n <= 3 * 10^4, same length"
    assert all(type(v) is int and -10**5 <= v <= 10**5 for v in postorder), "-10^5 <= value <= 10^5"
    assert len(set(postorder)) == len(postorder) and set(postorder) == set(inorder), "distinct values, same set"
    at = {v: i for i, v in enumerate(inorder)}
    pos = len(postorder) - 1
    stack = [(0, len(inorder) - 1)]
    while stack:
        lo, hi = stack.pop()
        if lo > hi:
            continue
        m = at[postorder[pos]]
        assert lo <= m <= hi, "the walks don't come from one tree"
        pos -= 1
        stack.append((lo, m - 1))
        stack.append((m + 1, hi))
