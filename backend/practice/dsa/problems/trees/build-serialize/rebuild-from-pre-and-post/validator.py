def validate(preorder, postorder):
    n = len(preorder)
    assert isinstance(preorder, list) and isinstance(postorder, list) and 1 <= n == len(postorder) <= 30_000, "1 <= n <= 3 * 10^4"
    assert sorted(preorder) == list(range(1, n + 1)) and sorted(postorder) == list(range(1, n + 1)), "permutations of 1..n"
    assert preorder[0] == postorder[-1], "the root comes first in pre-order and last in post-order"
    at = {v: i for i, v in enumerate(postorder)}
    pos = 0
    stack = [(0, n - 1)]
    while stack:
        lo, hi = stack.pop()
        assert pos < n and lo <= at[preorder[pos]] == hi, "the walks don't come from one tree"
        pos += 1
        if lo < hi:
            m = at[preorder[pos]]
            assert lo <= m < hi, "the walks don't come from one tree"
            if m + 1 <= hi - 1:
                stack.append((m + 1, hi - 1))
            stack.append((lo, m))
