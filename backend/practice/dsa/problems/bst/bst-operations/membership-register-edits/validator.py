from ren_check import tree, is_bst


def validate(root, ops):
    tree("root", root, 1000, -10**5, 10**5, distinct=True)
    assert is_bst(root), "the tree must be a valid binary search tree"
    assert isinstance(ops, list) and 1 <= len(ops) <= 1000, "1 <= ops.length <= 1000"
    for op in ops:
        assert isinstance(op, list) and len(op) == 2 and op[0] in (0, 1), "each op is [0, k] or [1, k]"
        assert type(op[1]) is int and -10**5 <= op[1] <= 10**5, "-10^5 <= k <= 10^5"
